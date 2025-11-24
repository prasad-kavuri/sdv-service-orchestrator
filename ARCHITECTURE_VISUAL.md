# SDV Service Orchestrator - Visual Architecture

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERFACE (React)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Deploy New   │  │ View Active  │  │ Monitor      │          │
│  │ Service      │  │ Services     │  │ Resources    │          │
│  └──────┬───────┘  └──────────────┘  └──────────────┘          │
└─────────┼────────────────────────────────────────────────────────┘
          │ HTTP POST /api/services
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                  ORCHESTRATION ENGINE (Flask)                    │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Step 1: Service Definition                            │    │
│  │  ┌───────────────────────────────────────────────┐    │    │
│  │  │ Service: "Map Rendering"                      │    │    │
│  │  │ Requirements:                                 │    │    │
│  │  │  - CPU: 2.0 cores                            │    │    │
│  │  │  - Memory: 4096 MB                           │    │    │
│  │  │  - GPU: Required                             │    │    │
│  │  │  - Bandwidth: 200 Mbps                       │    │    │
│  │  └───────────────────────────────────────────────┘    │    │
│  └────────────────────────────────────────────────────────┘    │
│                          │                                       │
│                          ▼                                       │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Step 2: Node Selection (Bin-Packing Algorithm)       │    │
│  │                                                         │    │
│  │  For each node:                                        │    │
│  │    ✓ Check CPU availability (>= 2.0 cores)            │    │
│  │    ✓ Check Memory availability (>= 4096 MB)           │    │
│  │    ✓ Check GPU presence (Required)                    │    │
│  │    ✓ Check Network bandwidth (>= 200 Mbps)            │    │
│  │    ✓ Calculate fitness score                          │    │
│  │                                                         │    │
│  │  Select node with best fit (tightest resource match)  │    │
│  └────────────────────────────────────────────────────────┘    │
│                          │                                       │
│                          ▼                                       │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Step 3: Resource Allocation                           │    │
│  │  - Reserve CPU cores on selected node                 │    │
│  │  - Reserve memory on selected node                    │    │
│  │  - Mark service as RUNNING                            │    │
│  │  - Track deployment on node                           │    │
│  └────────────────────────────────────────────────────────┘    │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    VEHICLE COMPUTE NODES                         │
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐ │
│  │  ADAS Domain     │  │  Infotainment    │  │  Telematics   │ │
│  │  Controller      │  │  Unit            │  │  Control Unit │ │
│  ├──────────────────┤  ├──────────────────┤  ├───────────────┤ │
│  │ CPU: 4 cores     │  │ CPU: 8 cores     │  │ CPU: 2 cores  │ │
│  │ RAM: 8192 MB     │  │ RAM: 16384 MB    │  │ RAM: 4096 MB  │ │
│  │ GPU: ✓ Yes       │  │ GPU: ✓ Yes       │  │ GPU: ✗ No     │ │
│  │ Network: 1000    │  │ Network: 1000    │  │ Network: 500  │ │
│  ├──────────────────┤  ├──────────────────┤  ├───────────────┤ │
│  │ Services:        │  │ Services:        │  │ Services:     │ │
│  │ • Traffic        │  │ • Map Rendering  │  │ • GPS         │ │
│  │   Analysis       │  │ • POI Search     │  │ • Route Plan  │ │
│  └──────────────────┘  └──────────────────┘  └───────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Service Deployment Flow

### Example: Deploying "Map Rendering Service"

```
Step 1: User Action
┌─────────────────────┐
│ User clicks         │
│ "Deploy Service"    │
│ button              │
└──────┬──────────────┘
       │
       ▼
Step 2: Backend Receives Request
┌─────────────────────┐
│ POST /api/services  │
│ {                   │
│   template:         │
│   "map_rendering"   │
│ }                   │
└──────┬──────────────┘
       │
       ▼
Step 3: Create Service Object
┌─────────────────────┐
│ LocationService(    │
│   name: "Map..."    │
│   cpu: 2.0          │
│   memory: 4096      │
│   gpu: true         │
│   status: PENDING   │
│ )                   │
└──────┬──────────────┘
       │
       ▼
Step 4: Orchestrator Evaluates Nodes
┌──────────────────────────────────────┐
│ Node 1 (ADAS):                       │
│ ✓ CPU: 4.0 available (need 2.0)     │
│ ✓ Memory: 8192 MB (need 4096)       │
│ ✓ GPU: Yes                           │
│ ✓ Fitness: 2.0 (available/required) │
│                                       │
│ Node 2 (Infotainment):               │
│ ✓ CPU: 8.0 available (need 2.0)     │
│ ✓ Memory: 16384 MB (need 4096)      │
│ ✓ GPU: Yes                           │
│ ✓ Fitness: 4.0                       │
│                                       │
│ Node 3 (Telematics):                 │
│ ✗ GPU: No (REQUIRED)                 │
│ → EXCLUDED                            │
│                                       │
│ SELECTED: Node 1 (ADAS)              │
│ Reason: Tightest fit (lowest score) │
└──────┬───────────────────────────────┘
       │
       ▼
Step 5: Deploy to Node
┌─────────────────────┐
│ ADAS Node:          │
│ Before:             │
│  CPU: 4.0 free      │
│  Memory: 8192 MB    │
│                     │
│ After:              │
│  CPU: 2.0 free      │
│  Memory: 4096 MB    │
│  Services: [        │
│    "Map Rendering"  │
│  ]                  │
└──────┬──────────────┘
       │
       ▼
Step 6: Update Service Status
┌─────────────────────┐
│ Service Status:     │
│ PENDING → RUNNING   │
│                     │
│ Deployed Node:      │
│ node-1 (ADAS)       │
└──────┬──────────────┘
       │
       ▼
Step 7: Frontend Updates
┌─────────────────────┐
│ UI shows:           │
│ ✓ Green "running"   │
│ ✓ Node assignment   │
│ ✓ Updated CPU bars  │
│ ✓ Service count     │
└─────────────────────┘
```

## Resource Utilization Example

### Before Deploying Services:
```
ADAS Controller          Infotainment Unit       Telematics Unit
┌──────────────┐        ┌──────────────┐        ┌──────────────┐
│ CPU: ░░░░    │ 0%     │ CPU: ░░░░    │ 0%     │ CPU: ░░░░    │ 0%
│ RAM: ░░░░    │ 0%     │ RAM: ░░░░    │ 0%     │ RAM: ░░░░    │ 0%
│ GPU: ✓       │        │ GPU: ✓       │        │ GPU: ✗       │
└──────────────┘        └──────────────┘        └──────────────┘
```

### After Deploying 5 Services:
```
ADAS Controller          Infotainment Unit       Telematics Unit
┌──────────────┐        ┌──────────────┐        ┌──────────────┐
│ CPU: ████░░  │ 63%    │ CPU: ███░░░  │ 44%    │ CPU: ██░░░░  │ 38%
│ RAM: ████░░  │ 69%    │ RAM: ███░░░  │ 50%    │ RAM: ███░░░  │ 50%
│ GPU: ✓       │        │ GPU: ✓       │        │ GPU: ✗       │
│              │        │              │        │              │
│ Services:    │        │ Services:    │        │ Services:    │
│ • Traffic    │        │ • Map        │        │ • GPS        │
│   Analysis   │        │   Rendering  │        │ • Route      │
│ • (empty)    │        │ • POI Search │        │   Planning   │
└──────────────┘        └──────────────┘        └──────────────┘
```

## Decision Tree: Where Should a Service Go?

```
                    New Service Arrives
                           │
                           ▼
                   ┌───────────────┐
                   │ Does it need  │
                   │ GPU?          │
                   └───┬───────┬───┘
                       │       │
                  YES  │       │  NO
                       │       │
         ┌─────────────┘       └─────────────┐
         ▼                                     ▼
    ┌────────────┐                      ┌────────────┐
    │ Filter to  │                      │ All nodes  │
    │ GPU nodes  │                      │ eligible   │
    │ (ADAS,     │                      │            │
    │ Infotain.) │                      │            │
    └─────┬──────┘                      └─────┬──────┘
          │                                    │
          └──────────────┬─────────────────────┘
                         ▼
                ┌────────────────┐
                │ Check resource │
                │ availability   │
                │ (CPU, Memory)  │
                └────┬───────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
   Enough       Enough       No resources
   on Node1     on Node2     available
        │            │            │
        ▼            ▼            ▼
   Fitness: 2.0  Fitness: 4.0  FAILED
   (BEST FIT!)   (OK)          deployment
        │
        ▼
   Deploy here!
```

## Real-World Analogy: Restaurant Kitchen

```
Service Request:          "Make Sushi"
(Map Rendering)          (Requires specialized station)

Kitchen Layout:
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│ ADAS Node      │  │ Infotainment   │  │ Telematics     │
│ (Sushi Bar)    │  │ (Main Kitchen) │  │ (Prep Station) │
├────────────────┤  ├────────────────┤  ├────────────────┤
│ • Sushi chef   │  │ • Multiple     │  │ • Basic prep   │
│   available    │  │   stations     │  │ • No special   │
│ • Rice cooker  │  │ • Oven, grill  │  │   equipment    │
│ • Fresh fish   │  │ • Sushi setup  │  │                │
└────────────────┘  └────────────────┘  └────────────────┘
       ↑                                         ↑
       │                                         │
    BEST FIT                                 CAN'T DO IT
  (specialized,                           (no equipment)
   less busy)

Head Chef Decision (Orchestrator):
"Send sushi order to Sushi Bar - they're equipped and have capacity"
```

This visual guide complements the technical documentation!
