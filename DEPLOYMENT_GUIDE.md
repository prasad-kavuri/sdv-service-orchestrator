# Deployment & Customization Guide

## 🚀 Quick Deploy Checklist

### Prerequisites
- [ ] Python 3.8+ installed
- [ ] Node.js 16+ and npm installed
- [ ] Terminal/Command Prompt access
- [ ] Ports 5000 and 3000 available

### Backend Setup (2 minutes)
```bash
cd sdv-service-orchestrator/backend
pip install -r requirements.txt
python app.py
```
✅ Success indicator: `Running on http://127.0.0.1:5000`

### Frontend Setup (3 minutes)
```bash
# New terminal window
cd sdv-service-orchestrator/frontend
npm install
npm start
```
✅ Success indicator: Browser opens to `http://localhost:3000`

### Verify Installation
- [ ] See 3 vehicle nodes displayed
- [ ] Deploy a service successfully
- [ ] Watch CPU bars update
- [ ] Undeploy service works

---

## 🎨 Customization Ideas

### 1. Add New Service Types

Edit `backend/app.py`, add to `SERVICE_TEMPLATES` (around line 60):

```python
"parking_assist": {
    "name": "Automated Parking Service",
    "type": "automation",
    "requirements": ResourceRequirements(
        cpu_cores=1.5,
        memory_mb=2048,
        gpu_required=True,
        network_bandwidth_mbps=100
    )
}
```

### 2. Add New Vehicle Nodes

Edit `backend/app.py` in `initialize_vehicle_nodes()` (around line 90):

```python
VehicleNode(
    id="node-4",
    name="Powertrain Control Module",
    domain="Powertrain",
    total_cpu=2.0,
    total_memory=2048,
    has_gpu=False,
    network_bandwidth=500,
    available_cpu=2.0,
    available_memory=2048,
    deployed_services=[]
)
```

### 3. Modify Scheduling Algorithm

Edit `Orchestrator.find_suitable_node()` (around line 100):

**Current**: Selects node with tightest fit
**Options**:
- Round-robin: `return nodes[counter % len(nodes)]`
- Least loaded: `sort by (available_cpu + available_memory)`
- Random: `return random.choice(suitable_nodes)`

### 4. Add Service Priorities

Add to `LocationService` class:
```python
priority: int = 5  # 1 (highest) to 10 (lowest)
```

Modify orchestrator to deploy high-priority services first.

### 5. Implement Auto-Scaling

Add to orchestrator:
```python
def auto_scale(service_type):
    if cpu_utilization > 80%:
        deploy_replica(service_type)
```

---

## 🌐 Advanced Deployment

### Docker Setup

Create `Dockerfile` in backend:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

Run: `docker-compose up`

### Add Database Persistence

Install: `pip install sqlalchemy`

Replace in-memory storage:
```python
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class ServiceModel(Base):
    __tablename__ = 'services'
    id = Column(String, primary_key=True)
    name = Column(String)
    status = Column(String)
    # ... other fields
```

### Deploy to Cloud

**AWS EC2**:
```bash
# Install dependencies on EC2 instance
sudo apt update
sudo apt install python3-pip nodejs npm
# Clone repo and follow quick start
```

**Heroku**:
```bash
heroku create sdv-orchestrator
git push heroku main
heroku open
```

**DigitalOcean App Platform**:
- Connect GitHub repo
- Configure buildpacks (Python + Node)
- Deploy automatically

---

## 🧪 Testing Scenarios

### Test 1: Resource Exhaustion
```bash
# Deploy multiple heavy services until failure
curl -X POST http://localhost:5000/api/services \
  -H "Content-Type: application/json" \
  -d '{"template": "traffic_analysis"}'
# Repeat until one fails
```

### Test 2: Load Balancing
```bash
# Deploy 10 lightweight services
for i in {1..10}; do
  curl -X POST http://localhost:5000/api/services \
    -H "Content-Type: application/json" \
    -d '{"template": "gps_positioning"}'
done
# Check node distribution
curl http://localhost:5000/api/nodes
```

### Test 3: Service Recovery
```bash
# Deploy service, note node assignment
# Kill backend (Ctrl+C)
# Restart backend
# Verify state is lost (demonstrates need for persistence)
```

---

## 📈 Performance Optimization

### Backend
- Add caching with `@lru_cache` for frequently called functions
- Use connection pooling for database
- Implement async endpoints with `async def`

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def calculate_fitness(node_id, service_id):
    # Expensive calculation
    pass
```

### Frontend
- Use React.memo for expensive components
- Implement virtualization for long service lists
- Add debouncing for API calls

```javascript
import { memo } from 'react';

const ServiceCard = memo(({ service }) => {
  // Component code
});
```

---

## 🐛 Troubleshooting

### Issue: "Port already in use"
**Solution**: Change ports in code or kill existing processes
```bash
# Find process using port 5000
lsof -i :5000
# Kill it
kill -9 <PID>
```

### Issue: "Module not found"
**Solution**: Verify all dependencies installed
```bash
pip list | grep Flask
npm list --depth=0
```

### Issue: "CORS error in browser"
**Solution**: Verify Flask-CORS installed and configured
```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # This line must be present
```

### Issue: Services deploy but UI doesn't update
**Solution**: Check browser console, verify polling interval
```javascript
// In App.js, verify this exists:
useEffect(() => {
  fetchData();
  const interval = setInterval(fetchData, 2000);
  return () => clearInterval(interval);
}, []);
```

---

## 📚 Next Steps

### Beginner
1. Run the app successfully
2. Deploy all 5 service types
3. Understand the architecture diagram
4. Modify a service template

### Intermediate
1. Add a new node type
2. Implement a different scheduling algorithm
3. Add service dependencies
4. Create health check endpoints

### Advanced
1. Add database persistence (PostgreSQL)
2. Implement WebSocket for real-time updates
3. Add authentication and authorization
4. Create Docker deployment
5. Add comprehensive unit tests
6. Implement service auto-scaling

---

## 🎯 Portfolio Integration

### GitHub Repository Structure
```
sdv-service-orchestrator/
├── README.md              (Project overview)
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── tests/
├── frontend/
│   ├── src/
│   ├── package.json
│   └── public/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── API_REFERENCE.md
│   └── DEPLOYMENT.md
├── docker-compose.yml
└── .github/
    └── workflows/
        └── ci.yml
```

### README Highlights
```markdown
# SDV Service Orchestrator

![Demo GIF](./demo.gif)

A production-ready demonstration of Software Defined Vehicle (SDV) 
service orchestration for location-based services.

## Live Demo
[View Demo](https://your-deployment-url.com)

## Tech Stack
Python | Flask | React | REST API | Microservices

## Key Features
✅ Intelligent bin-packing scheduler
✅ Real-time resource monitoring
✅ Heterogeneous compute management
✅ GPU-aware service placement
```

### Record a Demo
Use tools like:
- **Loom**: Screen recording with narration
- **OBS Studio**: Free, professional recording
- **QuickTime**: Mac built-in screen recording

Upload to YouTube and embed in README.

---

## ✅ Pre-Interview Checklist

- [ ] App runs without errors
- [ ] Can deploy all service types
- [ ] Understand the orchestration algorithm
- [ ] Can explain bin-packing vs other approaches
- [ ] Know the tradeoffs of in-memory storage
- [ ] Have 2-3 extension ideas ready
- [ ] Understand SDV domain context
- [ ] Can discuss real-world applications

Good luck with your interviews! 🚀
