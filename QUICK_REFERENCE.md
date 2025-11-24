# 🚀 Quick Reference Card

Keep this handy while working with the project!

## 📦 Local Development

### Starting the App
```bash
# Terminal 1: Backend
cd backend
python app.py

# Terminal 2: Frontend  
cd frontend
npm start
```

### Stopping the App
```bash
# In each terminal
Ctrl + C
```

### Restarting After Changes
```bash
# Backend changes: Just Ctrl+C and restart python app.py
# Frontend changes: Saves auto-reload, no restart needed
# Requirements changes: pip install -r requirements.txt
# Package.json changes: npm install
```

---

## 🧪 Testing URLs

| What | URL |
|------|-----|
| Frontend Dashboard | http://localhost:3000 |
| Backend API Health | http://localhost:5000/api/nodes |
| All Services | http://localhost:5000/api/services |
| System Stats | http://localhost:5000/api/stats |
| Service Templates | http://localhost:5000/api/templates |

---

## 📡 API Quick Test

```bash
# Get all nodes
curl http://localhost:5000/api/nodes

# Get all services
curl http://localhost:5000/api/services

# Deploy GPS service
curl -X POST http://localhost:5000/api/services \
  -H "Content-Type: application/json" \
  -d '{"template": "gps_positioning"}'

# Deploy Map Rendering
curl -X POST http://localhost:5000/api/services \
  -H "Content-Type: application/json" \
  -d '{"template": "map_rendering"}'

# Get system statistics
curl http://localhost:5000/api/stats
```

---

## 🔧 Common Fixes

### "Port already in use"
```bash
# macOS/Linux
lsof -i :5000
kill -9 <PID>

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### "Module not found"
```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend && npm install
```

### "CORS error"
- Verify Flask-CORS is installed: `pip list | grep Flask-CORS`
- Check `app.py` has: `CORS(app)`
- Restart backend

### "Frontend won't load"
- Check backend is running on port 5000
- Open browser console (F12) → Check Network tab
- Verify `package.json` has: `"proxy": "http://localhost:5000"`

---

## 🐙 Git Commands

### Initial Setup
```bash
git init
git add .
git commit -m "Initial commit: SDV Service Orchestrator"
git remote add origin https://github.com/YOUR_USERNAME/sdv-service-orchestrator.git
git push -u origin main
```

### Regular Updates
```bash
git status                    # See what changed
git add .                     # Stage all changes
git commit -m "Description"   # Commit with message
git push                      # Push to GitHub
```

### Undo Last Commit (if not pushed)
```bash
git reset HEAD~1
```

### Pull Latest from GitHub
```bash
git pull origin main
```

---

## 📝 File Locations

### Backend Files
```
backend/
├── app.py                    # Main logic (LINE 100: bin-packing algo)
└── requirements.txt          # Python dependencies
```

### Frontend Files
```
frontend/
├── package.json              # Node dependencies + proxy config
├── public/index.html         # HTML template
└── src/
    ├── App.js                # Main React component (LINE 35: deploy logic)
    ├── App.css               # Styling
    ├── index.js              # React entry point
    └── index.css             # Global styles
```

### Documentation
```
ROOT/
├── README.md                 # Main overview
├── QUICKSTART.md             # 5-min setup
├── INDEX.md                  # Doc navigator
├── GITHUB_CHECKLIST.md       # This file's location
└── ... 8 total docs
```

---

## 🎯 Service Templates Reference

| Template Key | Name | CPU | Memory | GPU | Bandwidth |
|-------------|------|-----|--------|-----|-----------|
| `gps_positioning` | GPS Positioning | 0.5 | 512 MB | ❌ | 50 Mbps |
| `map_rendering` | Map Rendering | 2.0 | 4096 MB | ✅ | 200 Mbps |
| `route_planning` | Route Planning | 1.5 | 2048 MB | ❌ | 100 Mbps |
| `poi_search` | POI Search | 1.0 | 1024 MB | ❌ | 150 Mbps |
| `traffic_analysis` | Traffic Analysis | 2.5 | 3072 MB | ✅ | 300 Mbps |

---

## 🚗 Vehicle Nodes Reference

| Node ID | Name | Domain | CPU | Memory | GPU |
|---------|------|--------|-----|--------|-----|
| `node-1` | ADAS Domain Controller | ADAS | 4.0 | 8192 MB | ✅ |
| `node-2` | Infotainment Unit | Infotainment | 8.0 | 16384 MB | ✅ |
| `node-3` | Telematics Control Unit | Telematics | 2.0 | 4096 MB | ❌ |

---

## 🎨 Customization Quick Edits

### Add New Service Template
**File:** `backend/app.py` (around line 60)
```python
"your_service": {
    "name": "Your Service Name",
    "type": "your_type",
    "requirements": ResourceRequirements(
        cpu_cores=1.0,
        memory_mb=1024,
        gpu_required=False,
        network_bandwidth_mbps=100
    )
}
```

### Add New Vehicle Node
**File:** `backend/app.py` in `initialize_vehicle_nodes()` (around line 90)
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

### Change Polling Interval
**File:** `frontend/src/App.js` (around line 25)
```javascript
const interval = setInterval(fetchData, 2000); // Change 2000 to desired ms
```

### Change Port
**Backend:** `backend/app.py` (last line)
```python
app.run(debug=True, port=5000)  # Change 5000
```

**Frontend:** `frontend/package.json`
```json
"proxy": "http://localhost:5000"  // Match backend port
```

---

## 📊 Demo Flow

1. **Open app** → See 3 nodes with 0% utilization
2. **Deploy "Map Rendering"** → Goes to ADAS (GPU + tight fit)
3. **Deploy "GPS Positioning"** → Goes to Telematics (no GPU needed)
4. **Deploy "Traffic Analysis" x2** → Fills GPU nodes
5. **Try 3rd Traffic** → FAILS (no GPU available)
6. **Undeploy one** → Resources freed
7. **Retry 3rd Traffic** → SUCCESS

**Time:** 2-3 minutes

---

## 🎤 Elevator Pitch (30 seconds)

*"I built an SDV service orchestrator that demonstrates how modern vehicles manage location services across distributed compute nodes. It uses a bin-packing algorithm to intelligently place services based on CPU, memory, and GPU requirements. The system has a Python backend with Flask and a React frontend that shows real-time resource utilization. It showcases concepts from production vehicle software like AUTOSAR and NVIDIA DRIVE."*

---

## 📞 Quick Help

| Issue | Solution |
|-------|----------|
| Won't start | Check prerequisites installed |
| Port in use | Kill process or change port |
| Frontend blank | Verify backend running, check console |
| Changes not showing | Hard refresh (Ctrl+Shift+R) |
| Git push fails | Check remote URL, credentials |
| Can't find file | Use `find . -name "filename"` |

---

## 🎯 Interview Questions Preview

**Q: "Explain the scheduling algorithm"**
A: "It's bin-packing - evaluates all nodes, filters by constraints, calculates fitness scores, selects tightest fit to prevent fragmentation."

**Q: "Why bin-packing over round-robin?"**
A: "Prevents resource fragmentation. Keeps high-capacity nodes available for large workloads by placing small services on smaller nodes first."

**Q: "How would you scale this?"**
A: "Add Redis for caching, PostgreSQL for persistence, message queue for async ops, horizontal scaling for API, and shard orchestrators by domain."

---

## ✅ Pre-Demo Checklist

- [ ] Backend running without errors
- [ ] Frontend displaying correctly
- [ ] Deployed at least 3 services successfully
- [ ] Understand bin-packing algorithm
- [ ] Can explain why GPU matters
- [ ] Know what ADAS/Infotainment/Telematics are
- [ ] Have 2-3 extension ideas ready

---

**💡 Tip:** Print this page or keep it open in a separate tab while working!

**⏱️ Last Updated:** November 2024
