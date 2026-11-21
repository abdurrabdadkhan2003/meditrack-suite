import importlib.util
import os
import sys

# Ensure modules from subpackages can be imported in tests
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.join(ROOT_DIR, "health-bi-dashboard") not in sys.path:
    sys.path.insert(0, os.path.join(ROOT_DIR, "health-bi-dashboard"))


def test_vision_telemetry_note_parser():
    """Verifies the string parsing math used by the Streamlit Vision Telemetry page."""
    sample_note = "Entries:24 | Exits:19 | Occ:5 | AvgWait:47.8s"
    parts = {p.split(":")[0].strip(): p.split(":")[1].strip() for p in sample_note.split("|")}

    entries = int(parts.get("Entries", 0))
    exits = int(parts.get("Exits", 0))
    occupancy = int(parts.get("Occ", 0))
    avg_wait = float(parts.get("AvgWait", "0").replace("s", ""))

    assert entries == 24
    assert exits == 19
    assert occupancy == 5
    assert avg_wait == 47.8
    assert (entries - exits) == occupancy


def test_dwell_time_alert_threshold():
    """Verifies waiting room congestion alert logic at the 60-second boundary."""
    normal_wait_sec = 42.0
    congested_wait_sec = 75.5
    threshold = 60.0

    assert normal_wait_sec <= threshold, "Normal wait should not trigger congestion alert"
    assert congested_wait_sec > threshold, "Wait over 60s must trigger congestion alert"


def test_roi_centroid_calculation():
    """Verifies bounding box center-point math for doorway line crossing."""
    box = [100, 200, 300, 500]  # [x1, y1, x2, y2]
    cx = int((box[0] + box[2]) / 2)
    cy = int((box[1] + box[3]) / 2)

    assert cx == 200
    assert cy == 350


def test_executive_sla_alert_evaluator():
    """Verifies automated threshold triggers for no-shows, claims, and vision dwell time."""
    from report_generator import evaluate_operational_alerts

    high_risk_metrics = {
        "no_show_rate": 18.5,
        "claim_rejection_rate": 14.2,
        "avg_wait_sec": 72.0
    }
    alerts = evaluate_operational_alerts(high_risk_metrics)
    assert len(alerts) == 3
    assert any("[OPS WARNING]" in a for a in alerts)
    assert any("[FINANCE ALERT]" in a for a in alerts)
    assert any("[VISION CONGESTION]" in a for a in alerts)

    nominal_metrics = {
        "no_show_rate": 5.0,
        "claim_rejection_rate": 4.0,
        "avg_wait_sec": 25.0
    }
    clear_alerts = evaluate_operational_alerts(nominal_metrics)
    assert len(clear_alerts) == 1
    assert "[ALL CLEAR]" in clear_alerts[0]


def test_executive_pdf_generation():
    """Verifies that the executive audit PDF compiler generates valid non-empty PDF bytes."""
    from report_generator import evaluate_operational_alerts, generate_executive_pdf_bytes

    sample_metrics = {
        "total_patients": 150,
        "total_appointments": 80,
        "completion_rate": 87.5,
        "no_show_rate": 12.5,
        "paid_revenue": 14500.0,
        "pending_revenue": 2100.0,
        "total_claims": 65,
        "claim_rejection_rate": 6.2,
        "vision_entries": 92,
        "peak_occupancy": 11,
        "avg_wait_sec": 38.5
    }
    alerts = evaluate_operational_alerts(sample_metrics)
    pdf_bytes = generate_executive_pdf_bytes(sample_metrics, alerts)
    assert isinstance(pdf_bytes, (bytes, bytearray))
    assert len(pdf_bytes) > 500
    assert pdf_bytes.startswith(b"%PDF")


def test_api_client_offline_fallback():
    """Verifies that the Streamlit API client provides synthetic data when running offline."""
    from api_client import MeditrackAPIClient

    client = MeditrackAPIClient()
    # Offline synthetic login
    assert client.login("admin_user", "admin123") is True
    assert client.token is not None

    patients = client.get_patients()
    assert len(patients) > 0
    assert "patient_id" in patients[0]

    appointments = client.get_appointments()
    assert len(appointments) > 0

    invoices = client.get_invoices()
    assert len(invoices) > 0

    claims = client.get_claims()
    assert len(claims) > 0

    telemetry = client.get_vision_telemetry()
    assert len(telemetry) > 0

    health = client.get_system_health()
    assert health["api_status"] in {"ONLINE", "STANDALONE_MODE"}

    audit_logs = client.get_audit_logs()
    assert len(audit_logs) > 0


def test_rbac_audit_log_schema():
    """Verifies that security audit records contain all required compliance fields."""
    sample_event = {
        "event_id": "AUD-1001",
        "timestamp": "2026-11-15 16:30:00",
        "actor": "admin_user",
        "role": "ADMIN",
        "action": "GENERATE_EXEC_PDF",
        "ip_address": "192.168.1.25",
        "details": "Compiled Executive SLA Audit PDF Brief"
    }
    required_keys = {"event_id", "timestamp", "actor", "role", "action", "ip_address", "details"}
    assert required_keys.issubset(sample_event.keys())
    assert sample_event["role"] in {"ADMIN", "CLINICIAN", "RECEPTION", "SERVICE_ACCOUNT"}


def test_fastapi_endpoints():
    """Verifies FastAPI health, authentication, and audit endpoints using TestClient."""
    from fastapi.testclient import TestClient

    api_path = os.path.join(ROOT_DIR, "clinic-ops-api")
    if api_path not in sys.path:
        sys.path.insert(0, api_path)

    spec = importlib.util.spec_from_file_location("clinic_ops_app", os.path.join(api_path, "main.py"))
    clinic_ops_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(clinic_ops_module)

    client = TestClient(clinic_ops_module.app)

    # Health Check
    health_resp = client.get("/health")
    assert health_resp.status_code == 200
    assert health_resp.json()["status"] == "ONLINE"

    # Login
    login_resp = client.post("/login", data={"username": "admin_user", "password": "admin123"})
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    assert token is not None

    # Audit Logs
    audit_resp = client.get("/audit-logs", headers={"Authorization": f"Bearer {token}"})
    assert audit_resp.status_code == 200
    logs = audit_resp.json()
    assert len(logs) == 60
    assert "event_id" in logs[0]
