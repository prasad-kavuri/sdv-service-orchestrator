# SDV Service Orchestrator - Technical Deep Dive

## Architecture Overview

This application demonstrates a **Software Defined Vehicle (SDV)** service orchestration system specifically for location-based services. It models how modern vehicles manage computational workloads across distributed ECUs (Electronic Control Units).

## Core Concepts

### 1. **Service Mapping** (What services exist)
Location services are defined with specific resource requirements:
- **GPS Positioning**: Low resource, no GPU needed
- **Map Rendering**: High resource, GPU required for visualization
- **Route Planning**: Medium CPU, no GPU needed
- **POI Search**: Moderate resources, network-heavy
- **Traffic Analysis**: High resource, GPU for ML inference

### 2. **Orchestration** (Where to deploy services)
The orchestrator uses a **bin-packing algorithm** to find optimal node placement:

```python
def find_suitable_node(service):
    # Check each node's available resources
    # Calculate fitness score (tighter fit = better)
    # Return best matching node
```

**Analogy**: Like a restaurant manager assigning dishes to kitchen stations based on what equipment each station has and what's currently available.

### 3. **Deployment** (Actually running services)
Once mapped, services are deployed by:
- Allocating CPU/memory resources
- Checking GPU availability if needed
- Tracking which services run on which nodes
- Monitoring real-time utilization

## Technical Implementation

### Backend (Python/Flask)

**Key Classes**:

1. **LocationService**: Represents a deployable service
   ```python
   - id: Unique identifier
   - name: Service name
   - requirements: CPU, memory, GPU, bandwidth
   - status: pending/running/failed
   - deployed_node: Which ECU it's running on
   ```

2. **VehicleNode**: Represents an ECU/compute domain
   ```python
   - domain: ADAS/Infotainment/Telematics
   - total_cpu/memory: Maximum capacity
   - available_cpu/memory: Currently free
   - deployed_services: List of running services
   ```

3. **Orchestrator**: Decision engine
   - `find_suitable_node()`: Finds best ECU for a service
   - `deploy_service()`: Allocates resources and starts service
   - `undeploy_service()`: Frees resources

**Scheduling Algorithm**:
```
For each service to deploy:
  1. Filter nodes with sufficient resources
  2. Check GPU requirement if needed
  3. Calculate fitness score = available/required
  4. Choose node with lowest fitness (tightest fit)
  5. Allocate resources and mark as deployed
```

### Frontend (React)

**Components**:
- **Stats Dashboard**: Real-time system metrics
- **Node Visualization**: Shows ECU utilization with progress bars
- **Service Deployment**: Interface to create new services
- **Service Monitoring**: List of deployed services with status

**Real-time Updates**: Polls backend every 2 seconds to refresh state

## SDV Domain Models

### ADAS Domain Controller
- **Purpose**: Advanced driver assistance (lane keeping, collision avoidance)
- **Resources**: 4 CPU cores, 8GB RAM, GPU enabled
- **Best for**: GPU-heavy tasks like traffic analysis, map rendering

### Infotainment Unit
- **Purpose**: User interface, entertainment, navigation
- **Resources**: 8 CPU cores, 16GB RAM, GPU enabled
- **Best for**: High-performance visualization, POI search

### Telematics Control Unit
- **Purpose**: Connectivity, cloud communication
- **Resources**: 2 CPU cores, 4GB RAM, no GPU
- **Best for**: Lightweight services like GPS positioning

## Example Scenarios

### Scenario 1: Normal Operation
```
1. User deploys "Map Rendering Service" (needs GPU)
2. Orchestrator evaluates: ADAS (4 cores, GPU) or Infotainment (8 cores, GPU)
3. Chooses Infotainment (more resources available)
4. Allocates 2 CPU cores, 4GB RAM
5. Service status: RUNNING
```

### Scenario 2: Resource Constraint
```
1. All GPU nodes are at capacity
2. User tries to deploy "Traffic Analysis" (needs GPU)
3. Orchestrator finds no suitable nodes
4. Service status: FAILED
5. User must undeploy another service first
```

### Scenario 3: Optimal Packing
```
1. Multiple lightweight services (GPS, POI Search)
2. Orchestrator places them on Telematics node (no GPU needed)
3. Saves GPU-capable nodes for heavy tasks
4. Efficient resource utilization across domains
```

## Key Features Demonstrated

✅ **Service Discovery**: Templated services with defined requirements
✅ **Resource-aware Scheduling**: CPU, memory, GPU, bandwidth constraints
✅ **Domain Separation**: Different vehicle ECUs with different capabilities
✅ **Real-time Monitoring**: Live utilization metrics and service health
✅ **Dynamic Lifecycle**: Deploy, monitor, undeploy services on-demand

## Extension Ideas

1. **Auto-scaling**: Deploy multiple instances when load increases
2. **Health Checks**: Restart failed services automatically
3. **Priority Scheduling**: Critical services get preference
4. **Load Balancing**: Distribute similar services across nodes
5. **Service Dependencies**: Ensure prerequisite services are running
6. **Over-subscription**: Allow overcommitting resources with limits

## Industry Context

This demo mirrors real SDV platforms like:
- **AUTOSAR Adaptive**: Service-oriented architecture for vehicles
- **Android Automotive**: App deployment on vehicle infotainment
- **NVIDIA DRIVE**: AI workload orchestration for autonomous vehicles
- **Tesla's Vehicle OS**: Dynamic service management

The core principles—service abstraction, resource orchestration, and domain separation—are fundamental to modern vehicle software architecture.
