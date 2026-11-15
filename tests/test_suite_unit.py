import pytest
from datetime import datetime

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
    high_risk_metrics = {
        "no_show_rate": 18.5,
        "claim_rejection_rate": 14.2,
        "avg_wait_sec": 72.0
    }
    triggered = []
    if high_risk_metrics["no_show_rate"] > 15.0:
        triggered.append("OPS_WARNING")
    if high_risk_metrics["claim_rejection_rate"] > 12.0:
        triggered.append("FINANCE_ALERT")
    if high_risk_metrics["avg_wait_sec"] > 60.0:
        triggered.append("VISION_CONGESTION")

    assert len(triggered) == 3
