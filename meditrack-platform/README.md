# Meditrack Clinical Operations & Vision Suite (`meditrack-platform`)

Master orchestration repository for Checklife Health Care Services. Unifies the relational database, RESTful backend API, interactive Streamlit BI portal, and YOLOv8 computer vision pipeline into a cohesive clinical analytics stack.

## System Architecture

```text
[ vision-patient-counter-poc ] (YOLOv8 + OpenCV Edge Node)
              │
              ▼ (HTTP POST /visits + JWT Bearer Token)
     [ clinic-ops-api ] ◄────────► [ meditrack-core-db ]
   (FastAPI + SQLAlchemy)             (PostgreSQL 15)
              ▲
              │ (REST JSON Payloads)
   [ health-bi-dashboard ]
 (Streamlit + Pandas + Plotly)
