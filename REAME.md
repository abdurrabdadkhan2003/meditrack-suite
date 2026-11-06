# Meditrack Clinical Operations & AI Vision Suite (`meditrack-suite`)

![CI Pipeline](https://github.com/abdurrabdadkhan2003/meditrack-suite/actions/workflows/ci_pipeline.yml/badge.svg)

End-to-end clinical operations, financial analytics, and computer vision waiting-room telemetry platform engineered for Checklife Health Care Services.

## Ecosystem Architecture
- **`meditrack-core-db` (`v1.0-db`)**: PostgreSQL 15 relational schema, SQL views, Alembic migrations, and synthetic data generators.
- **`clinic-ops-api` (`v1.0-api`)**: FastAPI REST backend with JWT authentication, RBAC permissions, and request latency logging middleware.
- **`health-bi-dashboard` (`v1.1-bi`)**: Multi-page Streamlit BI portal featuring Operational Footfall, Financial Claims, Audit CSV Exports, and Live Computer Vision Telemetry.
- **`vision-patient-counter-poc` (`v1.0-vision`)**: Ultralytics YOLOv8 + OpenCV pipeline tracking doorway entries/exits, polygonal ROI occupancy, and patient dwell times.
- **`meditrack-platform` (`v1.0-platform`)**: Master Docker Compose orchestration and E2E test suite.

## One-Command Developer CLI (`Makefile`)
- **Start Full Stack (Docker)**: `make up`
- **Run Unit & Integration Tests**: `make test`
- **Launch BI Dashboard Locally**: `make dashboard`
- **Run YOLOv8 Vision Tracker**: `make vision`
- **Stop All Containers**: `make down`
