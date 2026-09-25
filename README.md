# 🛡️ Mini-SIEM — Log Analysis & Threat Detection Dashboard

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?logo=sqlite)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-yellow)

> A lightweight **Security Information and Event Management (SIEM)** platform for log ingestion, normalization, threat detection, risk scoring, alert generation, and SOC-style security visualization — inspired by the analyst-oriented workflows of platforms like **Wazuh** and **Splunk**.

---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Security Notice](#-security-notice)
- [System Architecture](#-system-architecture)
- [Log Processing Pipeline](#-log-processing-pipeline)
- [Detection Workflow](#-detection-workflow)
- [Data Flow Diagrams (DFD)](#-data-flow-diagrams-dfd)
- [Database Design](#-database-design)
- [Features](#-features)
- [Detection Rules](#-detection-rules)
- [Risk Scoring](#-risk-scoring)
- [Project Structure](#-project-structure)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Testing](#-testing)
- [Sample Attack Scenarios](#-sample-attack-scenarios)
- [Screenshots](#-screenshots)
- [Team](#-team)
- [Development Workflow](#-development-workflow)
- [Limitations](#-limitations)
- [Future Scope](#-future-scope)
- [Academic Project Info](#-academic-project-info)

---

## 📖 Project Overview

**Mini-SIEM** is a web-based security monitoring and threat detection platform designed as an educational implementation of a simplified SIEM workflow.

The system collects logs from multiple sources — **Linux auth logs, web server logs, firewall logs, Windows event logs, and network/Nmap logs** — parses and normalizes them into a common event structure, stores them in a database, applies rule-based detection and correlation, calculates a risk score, generates alerts, and visualizes everything through a SOC-style analyst dashboard.

> Mini-SIEM is a lightweight, educational SIEM platform inspired by the analyst-oriented workflows of platforms such as Wazuh and Splunk. It focuses on log ingestion, normalization, rule-based threat detection, risk scoring, alert management, and SOC-style visualization. It does not claim to replace or replicate the full capabilities of either product.

---

## 🔒 Security Notice

This project is intended **only** for:

- Sample logs created by the project team
- Logs from systems owned or explicitly authorized for analysis
- Publicly available datasets permitted for security research

**Do not** use this project to analyze logs or systems without authorization.

---

## 🏗️ System Architecture

```text
LOG SOURCES
  Linux Auth Logs | Web Server Logs | Firewall Logs | Windows Event Logs | Network Logs (Nmap)
        │
        ▼
  LOG COLLECTOR  ──────────  Collects logs from multiple sources (Syslog, File, API)
        │
        ▼
     PARSER      ──────────  Parses different log formats (Apache, SSH, Windows, etc.)
        │
        ▼
  NORMALIZATION  ──────────  Converts to common event structure (JSON)
        │
        ▼
   DATABASE (SQLite)  ─────  Stores events, alerts and rules
        │
        ▼
  DETECTION ENGINE  ───────  Rule Evaluation │ Correlation │ Threshold Analysis │ Risk Scoring
        │
        ▼
  ALERT GENERATION  ───────  Creates security alerts with severity & score
        │
        ▼
  FASTAPI BACKEND   ───────  Provides REST APIs for the frontend
        │
        ▼
  SOC DASHBOARD     ───────  Visualizes logs, alerts, trends and investigations
        │
        ▼
  SECURITY ANALYST  ───────  Monitors, investigates and responds
```

---

## 🔄 Log Processing Pipeline

```text
1. Raw Log        (Syslog, Web, Windows, etc.)
        ↓
2. Parse          (Extract fields)
        ↓
3. Normalize      (Common format)
        ↓
4. Store          (SQLite)
        ↓
5. Analyze & Detect (Rules + Correlation)
        ↓
6. Score & Alert  (Risk Score + Severity)
        ↓
7. Visualize      (Dashboard)
```

---

## 🎯 Detection Workflow

```text
Event (from normalized logs)
        ↓
Rule Matching (check against rules)
        ↓
Correlation (cross-event analysis)
        ↓
Threshold Check (time window + count)
        ↓
   Threat Detected?
     /          \
   No            Yes
    │             │
Store Event   ┌───┴────────────┐
(normal log)  Risk Scoring   Alert Creation
              (calculate     (store & notify)
               score)
```

---

## 🔀 Data Flow Diagrams (DFD)

### DFD — Level 0 (Context Diagram)

```text
External Entities: Linux Server, Web Server, Firewall/Network, Security Analyst

Raw Logs ──────►  ┌───────────────────────────┐  ──────► Alerts / Reports
                   │        MINI-SIEM          │
                   │ Log Analysis & Threat     │ ◄────── Configuration / Investigation
                   │ Detection Dashboard       │           (Security Analyst)
                   └───────────────────────────┘
```

### DFD — Level 1

```text
Log Sources → 1. Log Collector → 2. Parser → 3. Normalization → 4. Database (SQLite)
            → 5. Detection Engine → 6. Alert Generation → 7. Dashboard
                                          ▲
                                   Security Analyst
```

### DFD — Level 2 (Detection Engine)

```text
Normalized Events
        ↓
Event Filtering
        ↓
Rule Evaluation
        ↓
Correlation
        ↓
Threat Pattern Identification
        ↓
   Match Found?
    /        \
  No          Yes ──► Store Event ──► Alert Creation ──► Alert Database ──► Dashboard
```

---

## 🗄️ Database Design

**Engine:** SQLite (can be migrated to PostgreSQL later)

| Table | Description |
|---|---|
| `events` | Stores all parsed log events |
| `alerts` | Stores generated security alerts |
| `rules` | Stores detection rules |
| `alert_events` | Links alerts with related events (many-to-many) |

**events**
`event_id (PK)`, `timestamp`, `source`, `host`, `src_ip`, `src_port`, `username`, `event_type`, `action`, `result`, `protocol`, `url`, `status_code`, `raw_message`

**alerts**
`alert_id (PK)`, `rule_id (FK)`, `timestamp`, `severity`, `risk_score`, `src_ip`, `title`, `description`, `event_count`, `status`

**rules**
`rule_id (PK)`, `rule_name`, `description`, `severity`, `threshold`, `time_window`, `enabled`

**alert_events**
`alert_id (FK)`, `event_id (FK)`, `relation_type`

**Relationships:** `rules (1) → alerts (N) → alert_events (N) → events (1)`

---

## ✨ Features

### Log Analysis
- Multi-source ingestion: Linux auth logs, web server logs, firewall logs, Windows event logs, network/Nmap logs
- Failed / accepted login detection
- IP, username, URL, and status code extraction
- Timestamp normalization
- Common event schema across all log sources

### Threat Detection
- SSH brute-force detection
- Multiple username attempts (account enumeration)
- Excessive HTTP 404 detection (web scanning)
- Time-based failed-login detection
- IP-based correlation across events

### Risk Scoring
- Transparent, rule-based scoring formula
- Automatic severity classification (LOW / MEDIUM / HIGH)

### SOC Dashboard
- KPI cards: **Total Events, Total Alerts, High Severity, Risk Score (Avg)**
- Events trend chart
- Alerts-by-severity donut chart
- Recent alerts table: Time, Rule ID, Title, Severity, Source IP, Status
- Event Explorer with filters (severity, source, IP, time range)
- Detection Rules management view
- Reports view
- Search and filtering across all views

---

## 🚨 Detection Rules

### 1. SSH Brute Force
```text
192.168.1.50
Failed login (x5+)
→ SSH_BRUTE_FORCE
```

### 2. Multiple Username Attempts
```text
192.168.1.50 → admin, root, test, guest
→ MULTIPLE_USERNAME_ATTEMPT
```

### 3. Excessive HTTP 404 (Web Scanning)
```text
192.168.1.60 → /admin, /backup, /config (all 404)
→ WEB_404_SCAN
```

### 4. Time-Based Brute Force
```text
5 failed logins within 10 minutes
→ TIME_BASED_BRUTE_FORCE
```

| Rule ID | Rule Name | Threshold | Time Window | Default Severity |
|---|---|---|---|---|
| SSH-001 | SSH Brute Force | 5 failed attempts | 10 min | HIGH |
| AUTH-002 | Multiple Username Attack | 3+ usernames | 10 min | MEDIUM |
| WEB-404 | Excessive 404 / Web Scan | 10 HTTP 404s | 5 min | MEDIUM |
| TIME-001 | Time-Based Brute Force | 5 failures | 10 min | HIGH |

---

## 📊 Risk Scoring

```text
Base Score
  + Failed Login Points
  + Multiple Username Points
  + 404 Points
  + Time-Window Points
```

| Score Range | Severity |
|---|---|
| 0–29 | 🟢 LOW |
| 30–59 | 🟡 MEDIUM |
| 60–100 | 🔴 HIGH |

---

## 📂 Project Structure

```text
mini-siem/
├── backend/
├── parser/
├── detection/
├── database/
├── dashboard/
├── data/
├── tests/
├── docs/
├── reports/
├── presentation/
├── scripts/
├── .github/
├── README.md
├── requirements.txt
└── run.py
```

> Full tree with every file is provided in `PROJECT_STRUCTURE.txt` for direct copy-paste into scaffolding scripts.

---

## 🧰 Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python, **FastAPI**, Uvicorn |
| Database | SQLite, SQLAlchemy |
| Frontend | HTML, CSS, JavaScript, Plotly |
| Parser / Log Tools | Regex, Pandas, Log Parsing |
| Testing | Pytest, HTTPX |
| Development | VS Code, Git / GitHub |
| OS & Environment | Ubuntu / Linux (Windows optional) |

> Note: earlier drafts of this project referenced a Flask backend. The finalized architecture diagram (system-architecture.png) specifies **FastAPI + Uvicorn** as the backend framework — this README follows that final decision. If your team keeps Flask instead, swap the install/run commands below accordingly.

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR-USERNAME/mini-siem.git
cd mini-siem
```

### 2. Create a virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the application

**FastAPI (final architecture):**
```bash
uvicorn backend.app:app --reload
```

**If still on Flask:**
```bash
python app.py
```

Then open:
```
http://127.0.0.1:8000        # FastAPI (default Uvicorn port)
http://127.0.0.1:5000        # Flask (if applicable)
```

Interactive API docs (FastAPI only):
```
http://127.0.0.1:8000/docs
```

---

## ▶️ Usage

1. Start the app with `uvicorn backend.app:app --reload`
2. Load sample logs from `data/raw/` (or supply your own authorized logs)
3. Open the SOC dashboard in your browser
4. Click **Refresh / Analyze** to run parsing + detection
5. Review KPI cards, events trend, and alerts-by-severity chart
6. Click into an alert for the full investigation view (Event Explorer)
7. Use the **Rules** page to review/adjust detection thresholds
8. Use the **Reports** page to export summary statistics

---

## 🧪 Testing

```bash
pytest                                   # all tests
pytest tests/test_auth_parser.py         # SSH parser
pytest tests/test_web_parser.py          # web parser
pytest tests/test_brute_force.py         # brute force rule
pytest tests/test_username_attack.py     # username enumeration rule
pytest tests/test_web_scan.py            # 404 scan rule
pytest tests/test_time_based.py          # time-window rule
pytest tests/test_api.py                 # FastAPI routes
pytest tests/test_integration.py         # full pipeline
```

### Test Matrix

| Test | Expected Result |
|---|---|
| Normal SSH login | No threat |
| 1 failed login | No threat |
| 5+ failed logins | Brute-force alert |
| Multiple usernames | Username attack alert |
| 10+ HTTP 404s | Web scanning alert |
| 5 failures / 10 min | Time-based alert |
| Empty log | No crash |
| Invalid log line | Skip / handle gracefully |
| Missing file | Proper error message |
| Multiple IPs | Separate detection per IP |

---

## 🎯 Sample Attack Scenarios

1. Normal authentication
2. SSH brute force
3. Multiple username attempts
4. Excessive HTTP 404 requests
5. Time-based brute force
6. Mixed security events

All testing is performed using authorized or synthetic log data only.

---

## 🖼️ Screenshots

> Add captured screenshots to `docs/screenshots/` and reference them below. The architecture/DFD/database diagrams live in `docs/architecture/`.

| View | Preview |
|---|---|
| Dashboard | `docs/screenshots/dashboard.png` |
| Events | `docs/screenshots/events.png` |
| Alerts | `docs/screenshots/alerts.png` |
| Alert Details | `docs/screenshots/alert-details.png` |
| Reports | `docs/screenshots/reports.png` |
| System Architecture | `docs/architecture/system-architecture.png` |
| DFD Level 0 / 1 / 2 | `docs/architecture/dfd-level-0.png`, `dfd-level-1.png`, `dfd-level-2.png` |
| Database ER Diagram | `docs/architecture/database-er-diagram.png` |

```markdown
![Dashboard](docs/screenshots/dashboard.png)
```

---

## 👥 Team

| Member | Role |
|---|---|
| **Vikash Kumar Jha** | Security Engineering, Integration & QA Lead |
| **Abhay Kumar** | SIEM Architecture & Backend Lead |
| **Shivani Kashyap** | Log Parsing & Normalization |
| **Aditya** | Threat Detection & Risk Scoring |
| **Bhanu** | SOC Dashboard & Frontend |

---

## 🔀 Development Workflow

```text
feature branch → commit → push → Pull Request → review → tests → develop → integration test → main
```

**Branches:**
```text
main
develop
feature/backend-abhay
feature/parser-shivani
feature/detection-aditya
feature/dashboard-bhanu
feature/testing-vikash
```

> ⚠️ No direct pushes to `main`. All merges require review from the Integration Lead (Abhay) and QA/Release Lead (Vikash).

---

## ⚠️ Limitations

This is an **educational Mini-SIEM implementation**. It does not attempt to reproduce the full capabilities, scalability, integrations, endpoint agents, threat intelligence ecosystem, or enterprise detection capabilities of commercial or full-featured SIEM platforms such as Wazuh or Splunk.

---

## 🚀 Future Scope

- Additional log sources (DNS, cloud audit logs)
- Threat intelligence & IP reputation integration
- GeoIP visualization
- Real-time log ingestion (WebSocket-based alert updates)
- Email/Slack notifications
- Authentication & role-based access control
- Docker deployment
- Elasticsearch / OpenSearch integration
- Machine-learning-based anomaly detection
- MITRE ATT&CK mapping

---

## 🎓 Academic Project Info

**Program:** B.Tech Cyber Security
**Semester:** VII
**Project:** Mini-SIEM — Log Analysis & Threat Detection Dashboard

Built for educational and authorized cybersecurity research purposes only.

---

## 📄 License

This project is released under the [MIT License](LICENSE) (or the license your team selects).
