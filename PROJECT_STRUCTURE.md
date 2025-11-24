# 📁 Project Structure

```
sdv-service-orchestrator/
│
├── 📄 README.md                    # Main project overview
├── 📄 QUICKSTART.md                # 5-minute setup guide
├── 📄 TECHNICAL_DETAILS.md         # Architecture deep dive
├── 📄 ARCHITECTURE_VISUAL.md       # Visual diagrams & flows
├── 📄 INTERVIEW_PREP.md            # How to present this
├── 📄 DEPLOYMENT_GUIDE.md          # Advanced deployment
├── 📄 DEMO_SCRIPT.md               # Live demo script
│
├── 🐍 backend/                     # Python/Flask Backend
│   ├── app.py                      # Main application (orchestrator logic)
│   └── requirements.txt            # Python dependencies
│
└── ⚛️ frontend/                    # React Frontend
    ├── package.json                # Node dependencies
    ├── public/
    │   └── index.html              # HTML template
    └── src/
        ├── App.js                  # Main React component
        ├── App.css                 # Styling
        ├── index.js                # React entry point
        └── index.css               # Global styles
```

## 📚 Documentation Guide

**Start Here:**
1. **README.md** - Project overview, tech stack, quick examples
2. **QUICKSTART.md** - Get the app running in 5 minutes

**Deep Dives:**
3. **TECHNICAL_DETAILS.md** - Architecture, algorithms, scenarios
4. **ARCHITECTURE_VISUAL.md** - Diagrams showing how everything connects

**Interview Prep:**
5. **INTERVIEW_PREP.md** - Talking points, Q&A prep, portfolio tips
6. **DEMO_SCRIPT.md** - Exact script for live presentations

**Advanced:**
7. **DEPLOYMENT_GUIDE.md** - Docker, cloud deployment, customization

## 🎯 Which Doc to Read When

**"I want to run this right now"**
→ QUICKSTART.md

**"I have an interview tomorrow"**
→ INTERVIEW_PREP.md + DEMO_SCRIPT.md

**"I need to understand the architecture"**
→ TECHNICAL_DETAILS.md + ARCHITECTURE_VISUAL.md

**"I want to deploy this to production"**
→ DEPLOYMENT_GUIDE.md

**"I want to add this to my portfolio"**
→ README.md + INTERVIEW_PREP.md

## 🔑 Key Files Explained

### Backend: `app.py` (Main Logic)

**Classes:**
- `ResourceRequirements` - CPU, memory, GPU, bandwidth specs
- `LocationService` - Represents a deployable service
- `VehicleNode` - Represents an ECU/compute domain
- `Orchestrator` - Core scheduling logic (★ MOST IMPORTANT)

**Key Methods:**
```python
Line ~90:  initialize_vehicle_nodes()  # Creates 3 vehicle nodes
Line ~100: find_suitable_node()         # ★ Bin-packing algorithm
Line ~130: deploy_service()             # Allocates resources
Line ~150: undeploy_service()           # Frees resources
Line ~170: API routes                   # REST endpoints
```

### Frontend: `App.js` (UI Logic)

**Key Sections:**
```javascript
Line ~10:  State management (nodes, services, stats)
Line ~15:  fetchData() - Polls backend every 2 seconds
Line ~35:  deployService() - POST to API
Line ~45:  deleteService() - DELETE to API
Line ~60:  Render logic - Stats, Nodes, Services
```

**Components:**
- Stats dashboard (3 cards showing metrics)
- Node cards (show each ECU with utilization)
- Service deployment controls (dropdown + button)
- Service list (deployed services with details)

## 📊 Data Flow

```
User clicks "Deploy Service"
         │
         ▼
    App.js: deployService()
         │
         ▼
    POST /api/services
         │
         ▼
    Flask Backend receives request
         │
         ▼
    Create LocationService object
         │
         ▼
    Orchestrator.find_suitable_node()
    ├── Filter by resources
    ├── Check GPU requirement
    ├── Calculate fitness scores
    └── Return best node
         │
         ▼
    Orchestrator.deploy_service()
    ├── Allocate CPU/memory
    ├── Update node state
    └── Set service status = RUNNING
         │
         ▼
    Return JSON response
         │
         ▼
    Frontend polls /api/services (every 2s)
         │
         ▼
    React updates UI
    ├── Service shows as "running"
    ├── Node CPU bar increases
    └── Service count increments
```

## 🧪 File Dependencies

```
Backend Dependencies (requirements.txt):
  Flask==3.0.0          # Web framework
  Flask-CORS==4.0.0     # Cross-origin requests

Frontend Dependencies (package.json):
  react@18.2.0          # UI library
  react-dom@18.2.0      # React renderer
  lucide-react@0.263.1  # Icon library
  react-scripts@5.0.1   # Build tooling
```

## 🚀 Execution Flow

### Backend Startup:
```python
1. Import dependencies (Flask, CORS, dataclasses)
2. Define domain types and service status enums
3. Create data models (LocationService, VehicleNode)
4. Initialize Orchestrator class with algorithms
5. Define service templates (5 location services)
6. Create API routes (GET/POST/DELETE)
7. Call initialize_vehicle_nodes() → Creates 3 nodes
8. Start Flask server on port 5000
```

### Frontend Startup:
```javascript
1. React loads index.js
2. Renders App.js component
3. useEffect triggers fetchData() on mount
4. Sets up interval (fetchData every 2s)
5. Initial API calls populate state
6. UI renders with fetched data
7. User interactions trigger API calls
8. State updates → UI re-renders
```

## 📝 Configuration Points

**Backend:**
- Port: `app.py` line ~260: `app.run(port=5000)`
- Node specifications: `initialize_vehicle_nodes()`
- Service templates: `SERVICE_TEMPLATES` dictionary
- Polling interval: `frontend/src/App.js` line ~25: `setInterval(fetchData, 2000)`

**Frontend:**
- Proxy: `package.json` → `"proxy": "http://localhost:5000"`
- Polling rate: `App.js` → `setInterval(fetchData, 2000)` # 2000ms
- Styling: `App.css` - colors, layouts, responsive breakpoints

## 🔧 Customization Checklist

To add a new service:
- [ ] Add to `SERVICE_TEMPLATES` in `app.py`
- [ ] Restart backend
- [ ] New service appears in frontend dropdown

To add a new node:
- [ ] Add to `initialize_vehicle_nodes()` in `app.py`
- [ ] Restart backend
- [ ] New node appears in frontend node list

To change scheduling algorithm:
- [ ] Modify `Orchestrator.find_suitable_node()` in `app.py`
- [ ] No frontend changes needed

To add persistence:
- [ ] Install SQLAlchemy: `pip install sqlalchemy`
- [ ] Replace in-memory dicts with database models
- [ ] Add migrations for schema management

## 💡 Quick Tips

**Debugging Backend:**
```bash
# Backend logs show in terminal
# Check for errors in orchestrator logic
python app.py  # Watch console output
```

**Debugging Frontend:**
```bash
# Open browser console (F12)
# Check Network tab for API calls
# Check Console tab for React errors
```

**Testing API Directly:**
```bash
curl http://localhost:5000/api/nodes
curl http://localhost:5000/api/stats
curl -X POST http://localhost:5000/api/services \
  -H "Content-Type: application/json" \
  -d '{"template": "gps_positioning"}'
```

## 🎓 Learning Path

**Beginner Level:**
1. Run the app successfully
2. Understand the 3-tier architecture (UI → API → Logic)
3. Deploy services and observe behavior
4. Read QUICKSTART.md and README.md

**Intermediate Level:**
5. Read through app.py line by line
6. Understand the bin-packing algorithm
7. Modify a service template
8. Read TECHNICAL_DETAILS.md

**Advanced Level:**
9. Add a new scheduling algorithm
10. Implement persistence layer
11. Add unit tests
12. Containerize with Docker

This is YOUR project now - customize it, extend it, make it yours! 🚀
