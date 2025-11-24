# 🚗 SDV Service Orchestrator

A production-ready demonstration of **Software Defined Vehicle (SDV)** service orchestration for location-based services. This project showcases intelligent service mapping, resource-aware scheduling, and real-time deployment management across heterogeneous vehicle compute domains.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![React](https://img.shields.io/badge/React-18.2-61dafb.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 What It Does

This application simulates how modern vehicles manage computational workloads across distributed ECUs (Electronic Control Units). It demonstrates:

- **Service Mapping**: Defining location services (GPS, Maps, Navigation) with resource requirements
- **Intelligent Orchestration**: Bin-packing algorithm for optimal service-to-node placement
- **Real-time Deployment**: Live resource allocation and monitoring
- **Domain Separation**: Heterogeneous compute nodes (ADAS, Infotainment, Telematics)

**Think of it like this**: Imagine a restaurant where the head chef (orchestrator) decides which dishes (services) should be prepared at which station (vehicle node) based on equipment availability and kitchen capacity.

## 🚀 Quick Start (5 Minutes)

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```

You should see:
```
🚗 SDV Service Orchestrator starting...
📍 Location services ready for deployment
 * Running on http://127.0.0.1:5000
```

### 2. Frontend Setup (New Terminal)
```bash
cd frontend
npm install
npm start
```

Browser opens automatically at `http://localhost:3000`

### 3. Try It!
1. Select "Map Rendering Service" from dropdown
2. Click "Deploy Service"
3. Watch it get assigned to a GPU-capable node
4. See real-time CPU utilization update
5. Deploy more services and observe intelligent placement

## 📸 Screenshots

```
┌─────────────────────────────────────────────────────────┐
│  SDV Service Orchestrator                                │
│  Location Services Deployment Management                 │
└─────────────────────────────────────────────────────────┘

┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ 3 Nodes      │  │ 5 Running    │  │ 67% CPU      │
└──────────────┘  └──────────────┘  └──────────────┘

┌─────────────────────────────────────────────────────────┐
│ ADAS Controller          Infotainment Unit              │
│ ████████░░ 75% CPU       ███████░░░ 63% CPU            │
│ GPU: ✓ Yes               GPU: ✓ Yes                     │
│ Services: 2              Services: 3                     │
└─────────────────────────────────────────────────────────┘
```

## 🏗️ Architecture

### High-Level Flow
```
┌─────────────────┐
│  User Interface │ (React Dashboard)
└────────┬────────┘
         │ HTTP POST /api/services
         ▼
┌─────────────────┐
│  Orchestrator   │ (Flask Backend)
│  - Find Node    │
│  - Allocate     │
│  - Track Status │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Vehicle Compute Nodes               │
│  ADAS | Infotainment | Telematics  │
└─────────────────────────────────────┘
```

### Scheduling Algorithm (Bin-Packing)
```python
1. Filter nodes with sufficient resources
2. Check GPU requirement if needed
3. Calculate fitness = available / required
4. Select node with lowest fitness (tightest fit)
5. Allocate resources and deploy
```

**Why bin-packing?** Prevents resource fragmentation by preferring tighter fits, leaving larger nodes available for bigger workloads.

## 🎓 Key Concepts Demonstrated

### 1. Service Definition
Each service has specific requirements:
```python
GPS_Positioning:      0.5 CPU, 512 MB, No GPU
Map_Rendering:        2.0 CPU, 4096 MB, GPU Required
Route_Planning:       1.5 CPU, 2048 MB, No GPU
Traffic_Analysis:     2.5 CPU, 3072 MB, GPU Required
```

### 2. Heterogeneous Nodes
Different vehicle domains have different capabilities:

| Domain | CPU | Memory | GPU | Use Case |
|--------|-----|--------|-----|----------|
| **ADAS** | 4 cores | 8 GB | ✅ Yes | Driver assistance, perception |
| **Infotainment** | 8 cores | 16 GB | ✅ Yes | Navigation, media, UI |
| **Telematics** | 2 cores | 4 GB | ❌ No | Connectivity, telemetry |

### 3. Resource-Aware Placement
Example: Deploying "Map Rendering Service"
- Requires GPU → Eliminates Telematics
- Needs 2 CPU cores → ADAS (4 free) vs Infotainment (8 free)
- Selects ADAS → Tighter fit (fitness: 2.0 vs 4.0)

## 📚 Documentation

- **[QUICKSTART.md](./QUICKSTART.md)** - Get running in 5 minutes
- **[TECHNICAL_DETAILS.md](./TECHNICAL_DETAILS.md)** - Deep dive into architecture
- **[ARCHITECTURE_VISUAL.md](./ARCHITECTURE_VISUAL.md)** - Visual diagrams and flows
- **[INTERVIEW_PREP.md](./INTERVIEW_PREP.md)** - How to present this project
- **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** - Customization and deployment

## 🛠️ Tech Stack

**Backend**:
- Python 3.8+ with Flask
- RESTful API design
- In-memory state management (easily extendable to PostgreSQL)
- CORS-enabled for frontend integration

**Frontend**:
- React 18 with Hooks
- Lucide Icons for beautiful UI
- Real-time polling (2-second intervals)
- Responsive design

**Architecture**:
- Microservices pattern
- Domain-driven design
- RESTful communication
- Stateless API

## 🎯 Example Use Cases

### Scenario 1: Smart Placement
```bash
# Deploy lightweight GPS service
POST /api/services {"template": "gps_positioning"}
→ Deploys to Telematics (no GPU needed, saves GPU nodes)

# Deploy GPU-heavy map rendering
POST /api/services {"template": "map_rendering"}
→ Deploys to Infotainment (GPU available, high capacity)
```

### Scenario 2: Resource Exhaustion
```bash
# Deploy 3 traffic analysis services (GPU-heavy)
# ADAS: Traffic Analysis #1 ✓
# Infotainment: Traffic Analysis #2 ✓
# Try to deploy Traffic Analysis #3 → FAILS (no GPU nodes left)

# Undeploy one service
DELETE /api/services/{service_id}
# Now Traffic Analysis #3 succeeds ✓
```

## 🧪 API Reference

### Get All Nodes
```bash
GET /api/nodes
```

### Get All Services
```bash
GET /api/services
```

### Deploy Service
```bash
POST /api/services
Content-Type: application/json

{
  "template": "map_rendering"
}
```

### Delete Service
```bash
DELETE /api/services/{service_id}
```

### Get System Stats
```bash
GET /api/stats
```

## 🔧 Customization

### Add New Service Template
Edit `backend/app.py`:
```python
SERVICE_TEMPLATES = {
    "your_service": {
        "name": "Your Service Name",
        "type": "custom",
        "requirements": ResourceRequirements(
            cpu_cores=1.0,
            memory_mb=1024,
            gpu_required=False,
            network_bandwidth_mbps=100
        )
    }
}
```

### Add New Vehicle Node
Edit `backend/app.py` in `initialize_vehicle_nodes()`:
```python
VehicleNode(
    id="node-4",
    name="Your Node Name",
    domain="YourDomain",
    total_cpu=4.0,
    total_memory=8192,
    has_gpu=True,
    network_bandwidth=1000,
    available_cpu=4.0,
    available_memory=8192,
    deployed_services=[]
)
```

## 📊 Real-World Applications

This architecture is used in:
- **AUTOSAR Adaptive Platform** - Standardized vehicle software
- **NVIDIA DRIVE OS** - Autonomous vehicle computing
- **Tesla Vehicle OS** - Dynamic workload management
- **Android Automotive** - In-vehicle app deployment

## 🚀 Future Enhancements

- [ ] Service auto-scaling based on load
- [ ] Persistent storage (PostgreSQL/Redis)
- [ ] Health checks and automatic restart
- [ ] Service dependencies and ordering
- [ ] WebSocket for real-time updates
- [ ] Docker containerization
- [ ] Kubernetes deployment
- [ ] Metrics and logging (Prometheus/Grafana)

## 🤝 Contributing

This is a portfolio/demo project, but feel free to:
1. Fork the repository
2. Add your enhancements
3. Share your improvements

## 📝 License

MIT License - feel free to use this for learning, portfolios, or interviews

## 👨‍💻 About

Built to demonstrate understanding of:
- Software Defined Vehicle architecture
- Resource scheduling algorithms
- Full-stack development
- System design principles
- Real-time monitoring systems

Perfect for showcasing in interviews for automotive software, embedded systems, or cloud/edge computing roles.

---

**Questions?** Check out the [INTERVIEW_PREP.md](./INTERVIEW_PREP.md) for talking points and demo flow!
