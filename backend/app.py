from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import uuid
from enum import Enum
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import random

app = Flask(__name__)
CORS(app)

# SDV Domain Types (like different kitchen stations)
class DomainType(Enum):
    ADAS = "ADAS"  # Advanced Driver Assistance
    INFOTAINMENT = "Infotainment"
    TELEMATICS = "Telematics"
    BODY_CONTROL = "Body Control"

# Service Status
class ServiceStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    FAILED = "failed"
    STOPPED = "stopped"

@dataclass
class ResourceRequirements:
    cpu_cores: float
    memory_mb: int
    gpu_required: bool
    network_bandwidth_mbps: int

@dataclass
class LocationService:
    id: str
    name: str
    type: str
    requirements: ResourceRequirements
    status: str
    deployed_node: Optional[str] = None
    created_at: str = ""
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'requirements': asdict(self.requirements),
            'status': self.status,
            'deployed_node': self.deployed_node,
            'created_at': self.created_at
        }

@dataclass
class VehicleNode:
    id: str
    name: str
    domain: str
    total_cpu: float
    total_memory: int
    has_gpu: bool
    network_bandwidth: int
    available_cpu: float
    available_memory: int
    deployed_services: List[str]
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'domain': self.domain,
            'total_cpu': self.total_cpu,
            'total_memory': self.total_memory,
            'has_gpu': self.has_gpu,
            'network_bandwidth': self.network_bandwidth,
            'available_cpu': self.available_cpu,
            'available_memory': self.available_memory,
            'deployed_services': self.deployed_services,
            'utilization': {
                'cpu': round((1 - self.available_cpu / self.total_cpu) * 100, 1),
                'memory': round((1 - self.available_memory / self.total_memory) * 100, 1)
            }
        }

# In-memory storage
vehicle_nodes = {}
services = {}

def initialize_vehicle_nodes():
    """Initialize vehicle ECUs/compute nodes"""
    nodes = [
        VehicleNode(
            id="node-1",
            name="ADAS Domain Controller",
            domain=DomainType.ADAS.value,
            total_cpu=4.0,
            total_memory=8192,
            has_gpu=True,
            network_bandwidth=1000,
            available_cpu=4.0,
            available_memory=8192,
            deployed_services=[]
        ),
        VehicleNode(
            id="node-2",
            name="Infotainment Unit",
            domain=DomainType.INFOTAINMENT.value,
            total_cpu=8.0,
            total_memory=16384,
            has_gpu=True,
            network_bandwidth=1000,
            available_cpu=8.0,
            available_memory=16384,
            deployed_services=[]
        ),
        VehicleNode(
            id="node-3",
            name="Telematics Control Unit",
            domain=DomainType.TELEMATICS.value,
            total_cpu=2.0,
            total_memory=4096,
            has_gpu=False,
            network_bandwidth=500,
            available_cpu=2.0,
            available_memory=4096,
            deployed_services=[]
        )
    ]
    
    for node in nodes:
        vehicle_nodes[node.id] = node

# Service templates for location services
SERVICE_TEMPLATES = {
    "gps_positioning": {
        "name": "GPS Positioning Service",
        "type": "positioning",
        "requirements": ResourceRequirements(cpu_cores=0.5, memory_mb=512, gpu_required=False, network_bandwidth_mbps=50)
    },
    "map_rendering": {
        "name": "Map Rendering Service",
        "type": "visualization",
        "requirements": ResourceRequirements(cpu_cores=2.0, memory_mb=4096, gpu_required=True, network_bandwidth_mbps=200)
    },
    "route_planning": {
        "name": "Route Planning Service",
        "type": "navigation",
        "requirements": ResourceRequirements(cpu_cores=1.5, memory_mb=2048, gpu_required=False, network_bandwidth_mbps=100)
    },
    "poi_search": {
        "name": "POI Search Service",
        "type": "discovery",
        "requirements": ResourceRequirements(cpu_cores=1.0, memory_mb=1024, gpu_required=False, network_bandwidth_mbps=150)
    },
    "traffic_analysis": {
        "name": "Real-time Traffic Analysis",
        "type": "analytics",
        "requirements": ResourceRequirements(cpu_cores=2.5, memory_mb=3072, gpu_required=True, network_bandwidth_mbps=300)
    }
}

class Orchestrator:
    """The brain of service deployment - like a head chef deciding which station cooks what"""
    
    @staticmethod
    def find_suitable_node(service: LocationService) -> Optional[VehicleNode]:
        """Find best node for service using bin-packing algorithm"""
        suitable_nodes = []
        
        for node in vehicle_nodes.values():
            # Check resource availability
            if (node.available_cpu >= service.requirements.cpu_cores and
                node.available_memory >= service.requirements.memory_mb and
                node.network_bandwidth >= service.requirements.network_bandwidth_mbps):
                
                # GPU check
                if service.requirements.gpu_required and not node.has_gpu:
                    continue
                
                # Calculate fitness score (prefer nodes with better resource match)
                cpu_fit = node.available_cpu / service.requirements.cpu_cores
                mem_fit = node.available_memory / service.requirements.memory_mb
                fitness = (cpu_fit + mem_fit) / 2
                
                suitable_nodes.append((fitness, node))
        
        if not suitable_nodes:
            return None
        
        # Return node with best fit (lowest fitness score = tightest fit)
        suitable_nodes.sort(key=lambda x: x[0])
        return suitable_nodes[0][1]
    
    @staticmethod
    def deploy_service(service: LocationService) -> bool:
        """Deploy service to a node"""
        node = Orchestrator.find_suitable_node(service)
        
        if not node:
            service.status = ServiceStatus.FAILED.value
            return False
        
        # Allocate resources
        node.available_cpu -= service.requirements.cpu_cores
        node.available_memory -= service.requirements.memory_mb
        node.deployed_services.append(service.id)
        
        service.deployed_node = node.id
        service.status = ServiceStatus.RUNNING.value
        
        return True
    
    @staticmethod
    def undeploy_service(service_id: str) -> bool:
        """Remove service from node and free resources"""
        if service_id not in services:
            return False
        
        service = services[service_id]
        if not service.deployed_node:
            return False
        
        node = vehicle_nodes.get(service.deployed_node)
        if not node:
            return False
        
        # Free resources
        node.available_cpu += service.requirements.cpu_cores
        node.available_memory += service.requirements.memory_mb
        node.deployed_services.remove(service_id)
        
        service.deployed_node = None
        service.status = ServiceStatus.STOPPED.value
        
        return True

# API Routes

@app.route('/api/nodes', methods=['GET'])
def get_nodes():
    """Get all vehicle nodes"""
    return jsonify([node.to_dict() for node in vehicle_nodes.values()])

@app.route('/api/services', methods=['GET'])
def get_services():
    """Get all services"""
    return jsonify([service.to_dict() for service in services.values()])

@app.route('/api/services', methods=['POST'])
def create_service():
    """Create and deploy a new service"""
    data = request.json
    template_key = data.get('template')
    
    if template_key not in SERVICE_TEMPLATES:
        return jsonify({'error': 'Invalid service template'}), 400
    
    template = SERVICE_TEMPLATES[template_key]
    service_id = str(uuid.uuid4())
    
    service = LocationService(
        id=service_id,
        name=template['name'],
        type=template['type'],
        requirements=template['requirements'],
        status=ServiceStatus.PENDING.value,
        created_at=datetime.now().isoformat()
    )
    
    services[service_id] = service
    
    # Try to deploy
    success = Orchestrator.deploy_service(service)
    
    return jsonify({
        'service': service.to_dict(),
        'deployed': success
    }), 201

@app.route('/api/services/<service_id>', methods=['DELETE'])
def delete_service(service_id):
    """Undeploy and delete a service"""
    if service_id not in services:
        return jsonify({'error': 'Service not found'}), 404
    
    Orchestrator.undeploy_service(service_id)
    del services[service_id]
    
    return jsonify({'message': 'Service deleted'}), 200

@app.route('/api/templates', methods=['GET'])
def get_templates():
    """Get available service templates"""
    return jsonify([
        {
            'key': key,
            'name': value['name'],
            'type': value['type'],
            'requirements': asdict(value['requirements'])
        }
        for key, value in SERVICE_TEMPLATES.items()
    ])

@app.route('/api/orchestrate', methods=['POST'])
def trigger_orchestration():
    """Manually trigger re-orchestration of all services"""
    # This could implement more complex scenarios like rebalancing
    pending_services = [s for s in services.values() if s.status == ServiceStatus.PENDING.value]
    
    deployed_count = 0
    for service in pending_services:
        if Orchestrator.deploy_service(service):
            deployed_count += 1
    
    return jsonify({
        'message': f'Deployed {deployed_count} pending services',
        'deployed_count': deployed_count
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall system statistics"""
    total_services = len(services)
    running_services = len([s for s in services.values() if s.status == ServiceStatus.RUNNING.value])
    failed_services = len([s for s in services.values() if s.status == ServiceStatus.FAILED.value])
    
    total_cpu = sum(n.total_cpu for n in vehicle_nodes.values())
    used_cpu = sum(n.total_cpu - n.available_cpu for n in vehicle_nodes.values())
    
    return jsonify({
        'services': {
            'total': total_services,
            'running': running_services,
            'failed': failed_services
        },
        'resources': {
            'cpu_utilization': round((used_cpu / total_cpu * 100), 1) if total_cpu > 0 else 0,
            'nodes': len(vehicle_nodes)
        }
    })

if __name__ == '__main__':
    initialize_vehicle_nodes()
    print("🚗 SDV Service Orchestrator starting...")
    print("📍 Location services ready for deployment")
    app.run(debug=True, port=5000)
