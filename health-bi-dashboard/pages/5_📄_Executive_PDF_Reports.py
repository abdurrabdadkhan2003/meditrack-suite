import streamlit as st
import pandas as pd
from datetime import datetime
from report_generator import evaluate_operational_alerts, generate_executive_pdf_bytes

st.set_page_config(page_title="Executive Reports", page_icon="📄", layout="wide")

if 'api' not in st.session_state or not st.session_state.api.token:
    st.warning("⚠️ Authentication required. Please log in from the main page.")
    st.stop()

api = st.session_state.api

st.title("📄 Executive PDF Briefing & Automated SLA Alerts")
st.markdown("Compile cross-platform operational, financial, and computer vision telemetry into a board-ready PDF audit brief.")

with st.spinner("Aggregating cross-module metrics..."):
    patients = api.get_patients()
    appointments = api.get_appointments()
    invoices = api.get_invoices()
    claims = api.get_claims()
    vision_logs = api.get_vision_telemetry()

df_appts = pd.DataFrame(appointments)
df_inv = pd.DataFrame(invoices)
df_claims = pd.DataFrame(claims)
df_vis = pd.DataFrame(vision_logs)

# Compute Consolidated Metrics
total_appts = len(df_appts)
completed_appts = len(df_appts[df_appts['status'] == 'COMPLETED']) if not df_appts.empty else 0
no_show_appts = len(df_appts[df_appts['status'] == 'NO_SHOW']) if not df_appts.empty else 0

paid_rev = float(df_inv[df_inv['status'] == 'PAID']['amount'].sum()) if not df_inv.empty else 0.0
pending_rev = float(df_inv[df_inv['status'] == 'ISSUED']['amount'].sum()) if not df_inv.empty else 0.0

total_claims = len(df_claims)
rejected_claims = len(df_claims[df_claims['status'] == 'REJECTED']) if not df_claims.empty else 0

metrics_summary = {
    "total_patients": len(patients),
    "total_appointments": total_appts,
    "completion_rate": (completed_appts / total_appts * 100) if total_appts > 0 else 0.0,
    "no_show_rate": (no_show_appts / total_appts * 100) if total_appts > 0 else 0.0,
    "paid_revenue": paid_rev,
    "pending_revenue": pending_rev,
    "total_claims": total_claims,
    "claim_rejection_rate": (rejected_claims / total_claims * 100) if total_claims > 0 else 0.0,
    "vision_entries": int(df_vis['entries'].max()) if not df_vis.empty else 0,
    "peak_occupancy": int(df_vis['occupancy'].max()) if not df_vis.empty else 0,
    "avg_wait_sec": float(df_vis['avg_wait_sec'].mean()) if not df_vis.empty else 0.0,
}

alerts = evaluate_operational_alerts(metrics_summary)

# --- Display Active Threshold Alerts ---
st.subheader("🔔 Automated SLA & Threshold Audit Status")
for alert in alerts:
    if "WARNING" in alert or "ALERT" in alert or "CONGESTION" in alert:
        st.warning(alert)
    else:
        st.success(alert)

st.markdown("---")

# --- Executive Snapshot Preview ---
st.subheader("📋 Consolidated Executive Snapshot")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("**Clinical Operations**")
    st.write(f"- Registered Patients: **{metrics_summary['total_patients']}**")
    st.write(f"- Completion Rate: **{metrics_summary['completion_rate']:.1f}%**")
    st.write(f"- No-Show Rate: **{metrics_summary['no_show_rate']:.1f}%**")

with c2:
    st.markdown("**Financial Health**")
    st.write(f"- Collected Revenue: **${metrics_summary['paid_revenue']:,.2f}**")
    st.write(f"- Pending Invoices: **${metrics_summary['pending_revenue']:,.2f}**")
    st.write(f"- Claim Rejection Rate: **{metrics_summary['claim_rejection_rate']:.1f}%**")

with c3:
    st.markdown("**YOLOv8 Vision Telemetry**")
    st.write(f"- Cumulative Entries: **{metrics_summary['vision_entries']}**")
    st.write(f"- Peak Waiting Occupancy: **{metrics_summary['peak_occupancy']} Patients**")
    st.write(f"- Mean Waiting Time: **{metrics_summary['avg_wait_sec']:.1f}s**")

st.markdown("---")

# --- One-Click PDF Export ---
pdf_bytes = generate_executive_pdf_bytes(metrics_summary, alerts)
file_stamp = datetime.now().strftime("%Y%m%d")

st.download_button(
    label="📥 Generate & Download Official Executive PDF Brief",
    data=pdf_bytes,
    file_name=f"Checklife_Executive_Brief_{file_stamp}.pdf",
    mime="application/pdf",
    use_container_width=True
)
