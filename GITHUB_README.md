# 🚗 SDV Service Orchestrator

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![React](https://img.shields.io/badge/React-18.2-61dafb.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

> A production-ready demonstration of Software Defined Vehicle (SDV) service orchestration for location-based services. Built to showcase intelligent service mapping, resource-aware scheduling, and real-time deployment management.

## ✨ Demo

![SDV Orchestrator Demo](https://via.placeholder.com/800x400/667eea/ffffff?text=Add+Your+Demo+GIF+Here)

*Replace the above with a GIF/screenshot of your running application*

## 🎯 What It Does

Simulates how modern vehicles manage computational workloads across distributed ECUs (Electronic Control Units):

- 🗺️ **Service Mapping** - Location services (GPS, Maps, Navigation) with resource requirements
- 🧠 **Intelligent Orchestration** - Bin-packing algorithm for optimal service-to-node placement  
- 📊 **Real-time Monitoring** - Live resource allocation and utilization tracking
- 🚗 **Domain Separation** - Heterogeneous compute nodes (ADAS, Infotainment, Telematics)

**Real-world analogy:** Like a restaurant head chef deciding which dishes (services) should be prepared at which station (vehicle node) based on equipment availability and kitchen capacity.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/sdv-service-orchestrator.git
cd sdv-service-orchestrator
```

2. **Start the Backend**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

Expected output: `🚗 SDV Service Orchestrator starting... * Running on http://127.0.0.1:5000`

3. **Start the Frontend** (new terminal)
```bash
cd frontend
npm install
npm start
```

Browser opens automatically at `http://localhost:3000`

4. **Try it out!**
   - Select "Map Rendering Service" from dropdown
   - Click "Deploy Service"
   - Watch it get assigned to a GPU-capable node
   - Observe real-time CPU utilization updates

## 🏗️ Architecture

```
┌─────────────────┐
│  React Frontend │  Real-time dashboard
└────────┬────────┘
         │ REST API
         ▼
┌─────────────────┐
│ Flask Backend   │  Orchestration engine
│  - Bin-packing  │  (Scheduling algorithm)
│  - Resource mgmt│
└────────┬────────┘
         │
         ▼
┌──────────────────────────────────┐
│     Vehicle Compute Nodes         │
│  ADAS | Infotainment | Telematics│
└──────────────────────────────────┘
```

### Scheduling Algorithm (Bin-Packing)

For each service deployment:
1. Filter nodes with sufficient CPU, memory, and network
2. Validate GPU requirement if needed
3. Calculate fitness score: `available_resources / required_resources`
4. Select node with **lowest fitness** (tightest fit)
5. Allocate resources and track deployment

**Why bin-packing?** Prevents resource fragmentation by preferring tighter fits, keeping larger nodes available for bigger workloads.

## 📊 Features

### Service Types
- **GPS Positioning** (0.5 CPU, 512MB, No GPU) - Basic location tracking
- **Map Rendering** (2.0 CPU, 4GB, GPU) - Visual map display  
- **Route Planning** (1.5 CPU, 2GB, No GPU) - Navigation computation
- **POI Search** (1.0 CPU, 1GB, No GPU) - Point of interest lookup
- **Traffic Analysis** (2.5 CPU, 3GB, GPU) - Real-time traffic ML

### Vehicle Nodes

| Domain | CPU | Memory | GPU | Purpose |
|--------|-----|--------|-----|---------|
| **ADAS** | 4 cores | 8 GB | ✅ | Driver assistance, perception |
| **Infotainment** | 8 cores | 16 GB | ✅ | Navigation, media, UI |
| **Telematics** | 2 cores | 4 GB | ❌ | Connectivity, telemetry |

## 🎨 Screenshots

*Add screenshots here showing:*
1. Main dashboard with node visualization
2. Service deployment in action
3. Resource utilization graphs

## 🧪 Example Scenarios

### Scenario 1: Smart Placement
```bash
# Deploy lightweight GPS (no GPU needed)
→ Goes to Telematics node (saves GPU nodes for heavy tasks)

# Deploy Map Rendering (GPU required)  
→ Goes to ADAS node (has GPU, tighter fit than Infotainment)
```

### Scenario 2: Resource Exhaustion
```bash
# Deploy 2 Traffic Analysis services (GPU-heavy)
# ADAS: Running Traffic Analysis ✓
# Infotainment: Running Traffic Analysis ✓

# Try to deploy 3rd Traffic Analysis
→ FAILS - No GPU nodes available

# Undeploy one service
→ Resources freed, 3rd deployment now succeeds ✓
```

## 🛠️ Tech Stack

- **Backend:** Python 3.8+, Flask 3.0, Flask-CORS
- **Frontend:** React 18, Lucide Icons
- **Architecture:** Microservices with REST API
- **State Management:** In-memory (production would use PostgreSQL/Redis)

## 📚 Documentation

- [Quick Start Guide](./QUICKSTART.md) - Get running in 5 minutes
- [Technical Details](./TECHNICAL_DETAILS.md) - Architecture deep dive
- [Visual Architecture](./ARCHITECTURE_VISUAL.md) - Diagrams and flows
- [Interview Prep](./INTERVIEW_PREP.md) - How to present this project
- [Deployment Guide](./DEPLOYMENT_GUIDE.md) - Customization and cloud deployment

## 🎯 Key Learnings

This project demonstrates:
- ✅ Full-stack development (Python + React)
- ✅ Algorithm implementation (bin-packing scheduler)
- ✅ System design (microservices, REST API)
- ✅ Real-time monitoring and state management
- ✅ Domain knowledge (SDV architecture, vehicle compute domains)

## 🚀 Future Enhancements

- [ ] Service auto-scaling based on load
- [ ] Persistent storage (PostgreSQL)
- [ ] WebSocket for real-time updates (remove polling)
- [ ] Service health checks and auto-restart
- [ ] Docker containerization
- [ ] Kubernetes deployment manifests
- [ ] Prometheus metrics + Grafana dashboards
- [ ] Authentication and authorization

## 🤝 Contributing

This is a portfolio/demo project, but suggestions are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by production SDV platforms (AUTOSAR Adaptive, NVIDIA DRIVE OS)
- Built as a portfolio piece to demonstrate automotive software expertise
- Scheduling algorithm based on classic bin-packing problem

## 📧 Contact

**Prasad Kavuri**
- Portfolio: [prasadkavuri.com](https://prasadkavuri.com)
- GitHub: [@YOUR_GITHUB_USERNAME](https://github.com/YOUR_GITHUB_USERNAME)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/YOUR_PROFILE)

---

⭐ **Star this repo** if you found it helpful for learning SDV concepts or interview preparation!

**Built with ❤️ for the automotive software community**
