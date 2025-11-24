# Quick Start Guide - SDV Service Orchestrator

## What You'll See

A live dashboard showing:
- 3 Vehicle compute nodes (ADAS, Infotainment, Telematics)
- Real-time CPU/memory utilization
- Location services you can deploy with one click
- Visual representation of which services run on which nodes

## Setup (5 minutes)

### 1. Backend Setup
```bash
cd sdv-service-orchestrator/backend
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
cd sdv-service-orchestrator/frontend
npm install
npm start
```

Browser will open automatically at `http://localhost:3000`

## Try It Out

### Basic Flow:
1. **View the 3 vehicle nodes** - each with different capabilities
2. **Select a service** from dropdown (try "Map Rendering Service")
3. **Click "Deploy Service"** - watch it get assigned to a node
4. **See real-time updates** - CPU bars fill up as you deploy more
5. **Deploy multiple services** - watch the orchestrator pick optimal nodes
6. **Undeploy services** - resources get freed immediately

### Interesting Experiments:

**Experiment 1**: Resource Exhaustion
- Deploy 2-3 "Traffic Analysis" services (GPU + CPU heavy)
- Try deploying a 4th - it will fail (no GPU nodes left)
- Undeploy one, then retry - now it succeeds!

**Experiment 2**: Smart Placement
- Deploy "GPS Positioning" (lightweight, no GPU)
- Notice it goes to Telematics node (saving GPU nodes for heavy tasks)
- Deploy "Map Rendering" (GPU required)
- Notice it goes to ADAS or Infotainment (has GPU)

**Experiment 3**: Resource Visualization
- Deploy services one by one
- Watch CPU utilization bars grow in real-time
- See how the orchestrator distributes load across nodes

## Architecture at a Glance

```
┌─────────────────────────────────────┐
│   Location Service Templates        │
│  (GPS, Maps, Navigation, Traffic)   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│      Orchestrator (Brain)           │
│  - Analyzes resource requirements   │
│  - Finds suitable node              │
│  - Allocates resources              │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│      Vehicle Compute Nodes          │
│  ADAS │ Infotainment │ Telematics  │
└─────────────────────────────────────┘
```

## Key Files to Explore

**Backend Logic**:
- `backend/app.py` - Line 90: `Orchestrator.find_suitable_node()` - This is where the magic happens! Bin-packing algorithm that decides placement.

**Frontend Visualization**:
- `frontend/src/App.js` - Line 130: Node rendering with real-time utilization

**Service Templates**:
- `backend/app.py` - Line 60: `SERVICE_TEMPLATES` - Define your own services here!

## API Endpoints

Test directly with curl:

```bash
# Get all nodes
curl http://localhost:5000/api/nodes

# Get all services
curl http://localhost:5000/api/services

# Deploy a service
curl -X POST http://localhost:5000/api/services \
  -H "Content-Type: application/json" \
  -d '{"template": "gps_positioning"}'

# Get statistics
curl http://localhost:5000/api/stats
```

## Troubleshooting

**Port already in use?**
- Backend: Change port in `backend/app.py` line 256: `app.run(port=5001)`
- Frontend: Edit `frontend/package.json` proxy to match

**Services won't deploy?**
- Check backend console for errors
- Ensure all nodes aren't at capacity (undeploy some services)

**Frontend won't connect?**
- Verify backend is running on port 5000
- Check browser console for network errors

## Next Steps

1. **Read TECHNICAL_DETAILS.md** - Deep dive into architecture
2. **Modify service templates** - Add your own location services
3. **Add new nodes** - Create more vehicle domains
4. **Implement auto-scaling** - Automatically deploy replicas
5. **Add service dependencies** - Ensure prerequisite services run first

## Interview Talking Points

- "Built orchestration engine using bin-packing algorithm"
- "Implemented resource-aware scheduling across heterogeneous ECUs"
- "Created real-time monitoring dashboard with React"
- "Demonstrated domain separation (ADAS, Infotainment, Telematics)"
- "Modeled SDV service lifecycle management"

Enjoy exploring! 🚗✨
