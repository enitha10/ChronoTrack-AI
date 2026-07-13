--> ChronoTrack AI

**Dynamic Ledger & Spatial Re-ID System for Automated Facility Occupancy Tracking**

Team GRAVITY | Department of Artificial Intelligence and Data Science | Bannari Amman Institute of Technology

--> Overview

ChronoTrack AI is a privacy-conscious, vision-based building monitoring system built for libraries and similar facilities. It maintains a real-time, dynamic inventory of active occupants and instantly pinpoints the spatial location of anyone remaining inside during closing or lockdown protocols — without relying on manual sweeps, RFID tags, or stored personal data.
Instead of slow sequential database queries, the system uses an **edge-based analytics pipeline** for real-time inference paired with a **dynamic hash-map lookup architecture** for instant, order-independent identity matching.

-->  Why it exists
Traditional facility management has three recurring problems:

1. **Manual evacuation sweeps** — staff must physically search multi-story buildings and hidden alcoves at closing time, which is slow and error-prone.
2. **Lagging accountability data** — standard gate counters give aggregate foot-traffic numbers but can't say *who* is in the building or *where*.
3. **Flawed sequential tracking** — existing logging systems use strict FIFO/LIFO queues, which break down because real-world exit patterns are non-sequential.

ChronoTrack AI solves this by replacing sequential logging with an **unordered hash-based occupancy set**, giving O(1) average-case insertion, lookup, and deletion regardless of exit order.

-->  How It Works

**Phase** 1 — Ingress Authentication (Dynamic Push)
- An entrance camera detects faces and converts each one into a 128-dimensional embedding vector — no raw photos or personal data are stored.
- Each person is assigned an anonymous token, pushed into a hash-map-backed active occupancy set in O(1) time.

**Phase 2** — Egress Reconciliation (Dynamic Pop)
- Exit cameras capture patrons as they leave and match faces against the active token set.
- On a match, the corresponding token is immediately deleted (O(1)), keeping the live occupancy count accurate to the second and avoiding unnecessary data retention.

**Phase 3** — Lockdown & Spatial Localisation
- At closing time (or on manual trigger), the system checks the active set size `N`.
- If `N = 0`, the building is confirmed clear.
- If `N > 0`, a parallelised Person Re-Identification (Re-ID) pipeline scans internal CCTV streams using facial matching, body geometry, and clothing histograms, then maps matches to physical zones — e.g. *"Alert: 2 occupants remain. ID_892 is located in the 3rd Floor East Reading Room."*

--> Technologies Used

| Component | Technology | Rationale |
| Video Capture & GUI | OpenCV (`opencv-python`) | Reads live webcam/CCTV frames, draws bounding boxes, and handles key inputs |
| Facial AI Inference | `face_recognition` | Detects faces and generates 128-D embedding vectors for identification |
| Visual Attribute Extraction | Channel Pixel Array Extraction (OpenCV) | Lightweight pixel-math thresholding to detect upper-torso/clothing color without a heavy secondary model |
| Search & Management Logic | O(1) Hash Map (Python `dict`) | Constant-time check-in/check-out regardless of exit order |
| Live UI Dashboard | Terminal interface (`os`, `time`) | Zero-latency, auto-refreshing occupancy dashboard without a web framework |

--> Dataset

ChronoTrack AI is currently in the proposed/development stage and does not yet use a proprietary dataset. Development and validation rely on established public benchmarks:
**Face Detection & Recognition**
- **LFW (Labelled Faces in the Wild)** — validates facial embedding and matching thresholds
- **CASIA-WebFace / VGGFace2** — used for pretraining/fine-tuning the embedding model

**Person Re-Identification & Tracking**
- **Market-1501** — benchmark for cross-camera pedestrian re-identification
- **MOT17 / MOT20** — validates tracking continuity (DeepSORT/YOLOv8) across occlusions and blind spots

For pilot deployment, a small, consent-based dataset from the library's entry/exit points will be used to calibrate thresholds for local lighting and camera conditions.

--> Prerequisites

- **OS:** Windows (PowerShell environment)
- **Python 3.11**
- **Git**
- 
--> Installation & Setup

1. **Navigate to the project workspace**
   powershell
   cd C:\Users\<your-username>\OneDrive\Desktop\cv

2. **Create and activate a virtual environment**
   powershell
   python -m venv venv311
   .\venv311\Scripts\Activate.ps1

3. **Install dependencies**
   powershell
   python -m pip install --upgrade pip
   pip install opencv-python face-recognition

4. **Configure camera sources**
   Update `config.yaml` with the RTSP/USB camera indices for entry, exit, and internal zone cameras, along with their mapped physical zone labels.

5. **Run the pipeline** (ingress → egress → dashboard → lockdown)

6. **Launch the staff alert dashboard**
   powershell
   python dashboard.py
   
   Then open the printed local URL in a browser.

--> Usage

### Normal Operation
- The system runs continuously during operating hours, silently registering entries (push) and exits (pop) — no staff intervention needed.
- Staff can view the live occupancy counter on the dashboard at any time.

--> Closing / Lockdown Audit

1. At closing time, the administrator clicks **"Run Closing Audit"** on the dashboard, or runs:
   powershell
   python dashboard.py
   python lockdown.py

2. The system reports every person's exit status by ID.
3. If anyone is still inside, an alert (red light + notification) is triggered, e.g. *"1 person is actively inside."*
4. The administrator runs the **Lockdown Audit** (`python lockdown.py`), which:
   - Identifies the remaining person(s) and their ID
   - Detects clothing color and matches the face against the entry image
   - Reports their last known location
5. Staff physically verify the flagged zone(s). Once confirmed clear, the operator marks the audit complete, resetting the active set for the next day.

--> Sample Output

**Live Dashboard**

CHRONOTRACK AI - LIVE LIBRARY MANAGEMENT DASHBOARD
=====================================================
► TOTAL STUDENT TOKENS LOGGED TODAY : 14
► CURRENT ACTIVE REAL-TIME OCCUPANCY: 1

[STATUS] 🔴 ZONE OCCUPIED: 1 student(s) actively inside.

Active Occupants Inside (1):
  • Student Token ID: ID_114 [STATUS: ACTIVE INSIDE]

Clear Egress History (13):
  • Student Token ID: ID_101 [STATUS: SAFELY EXITED]
  • ... (ID_102 – ID_113)


**Lockdown Audit**

CHRONOTRACK AI: MULTI-MODAL SPATIAL LOCALIZATION AUDIT
=====================================================
[ALERT] SECURITY BREACH: 1 occupant(s) remain inside!

▶ TARGET TRACKED   : ID_114
  ├─ Visual Profile: Face Vector Matched
  ├─ Dress Feature : Detected wearing [Mixed / Casual] clothing
  ├─ Last Location : Camera 70
  └─ Target Coordinates: 3rd Floor East Reading Room

--> Expected Outcomes (Pilot Phase)
- **Occupancy Accuracy** — live digital headcount matched against physical headcount, calibrated using LFW/VGGFace2 benchmarks
- **Sub-Second Latency** — entry/exit processing in under a second (O(1) efficiency)
- **Precision Zone Tracking** — accuracy of locating remaining occupants, validated against Market-1501/MOT standards
- **Threshold Calibration** — balances false matches against false non-matches

--> Dashboard States
- **State 1 — Live Occupancy Counter:** real-time count of anonymous guests inside
- **State 2 — "Building Clear" Confirmation:** triggers automatically when the active set hits zero
- **State 3 — Emergency Lockdown Alert:** live map of remaining anonymous IDs with last known zones

--> Future Scope

1. **Advanced Low-Light Tracking** — combine gait analysis and thermal imaging for dim areas like archives or basements.
2. **Edge Device Deployment** — run inference directly on smart cameras (e.g. NVIDIA Jetson) to improve privacy and speed.
3. **Smart Emergency Integration** — connect directly to fire alarms/emergency systems to push occupant lists to first responders.
4. **Privacy-First Space Analytics** — aggregate long-term foot-traffic patterns without storing individual user data.
5. **Mobile Alerts for Patrolling Staff** — push real-time zone alerts to a mobile app for staff on the move.
6. **Decentralized AI Updates (Federated Learning)** — improve model accuracy by training locally on-device rather than centralizing biometric data.

--> References

1. Huang, G. B., Ramesh, M., Berg, T., & Learned-Miller, E. (2007). *Labelled Faces in the Wild: A Database for Studying Face Recognition in Unconstrained Environments.* University of Massachusetts, Amherst.
2. Zheng, L., Shen, L., Tian, L., Wang, S., Wang, J., & Tian, Q. (2015). *Scalable Person Re-identification: A Benchmark (Market-1501).* IEEE ICCV.
3. Wojke, N., Bewley, A., & Paulus, D. (2017). *Simple Online and Real-time Tracking with a Deep Association Metric (DeepSORT).* IEEE ICIP.
4. Jocher, G., et al. *Ultralytics YOLOv8 Documentation.* https://docs.ultralytics.com
5. King, D. E. (2009). *Dlib-ml: A Machine Learning Toolkit.* Journal of Machine Learning Research.
6. Bradski, G. (2000). *The OpenCV Library.* Dr Dobb's Journal of Software Tools.
7. Redis Documentation. https://redis.io/docs/

--> Team Details: 

**GRAVITY** — Department of Artificial Intelligence and Data Science, Bannari Amman Institute of Technology (AY 2026–2027)

- Enitha P S — 7376242AD159
- Afritha Shirin S — 7376242AD112
- Deepika J — 7376242AD138
