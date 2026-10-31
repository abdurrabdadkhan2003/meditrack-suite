import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Vision Telemetry", page_icon="📹", layout="wide")

if 'api' not in st.session_state or not st.session_state.api.token:
    st.warning("⚠️ Authentication required. Please log in from the main page.")
    st.stop()

api = st.session_state.api

st.title("📹 Computer Vision Waiting Room Telemetry")
st.markdown("Live footfall, doorway line-crossing counts, and polygonal ROI dwell-time metrics streamed from `vision-patient-counter-poc` (YOLOv8).")

with st.spinner("Syncing YOLOv8 telemetry stream..."):
    telemetry_data = api.get_vision_telemetry()

df_vis = pd.DataFrame(telemetry_data)
df_vis['timestamp'] = pd.to_datetime(df_vis['timestamp'])
df_vis = df_vis.sort_values('timestamp')

latest = df_vis.iloc[-1]
peak_occ = df_vis['occupancy'].max()
overall_avg_wait = df_vis['avg_wait_sec'].mean()

# --- Row 1: Live Vision KPIs ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Live Waiting Room Occupancy", f"{latest['occupancy']} Patients")
col2.metric("Peak Occupancy Recorded", f"{peak_occ} Patients")
col3.metric("Cumulative Clinic Entries", int(latest['entries']))
col4.metric("Mean Waiting Dwell Time", f"{overall_avg_wait:.1f}s")

if latest['avg_wait_sec'] > 60:
    st.error(f"🚨 Congestion Alert: Current average wait time ({latest['avg_wait_sec']}s) exceeds the 60s threshold.")
else:
    st.success("✅ Waiting room flow is operating within normal dwell-time thresholds.")

st.markdown("---")

# --- Row 2: Telemetry Charts ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("Waiting Room Occupancy Over Time (Polygonal ROI)")
    fig_occ = px.area(
        df_vis,
        x='timestamp',
        y='occupancy',
        labels={'timestamp': 'Time', 'occupancy': 'Active Patients in Zone'},
        template="plotly_white",
        color_discrete_sequence=['#1976d2']
    )
    st.plotly_chart(fig_occ, use_container_width=True)

with c2:
    st.subheader("Average Patient Dwell Time Trend")
    fig_wait = px.line(
        df_vis,
        x='timestamp',
        y='avg_wait_sec',
        markers=True,
        labels={'timestamp': 'Time', 'avg_wait_sec': 'Avg Wait Time (Seconds)'},
        template="plotly_white",
        color_discrete_sequence=['#d32f2f']
    )
    fig_wait.add_hline(y=60, line_dash="dash", line_color="orange", annotation_text="60s Alert Threshold")
    st.plotly_chart(fig_wait, use_container_width=True)

st.markdown("---")
st.subheader("Raw Vision Telemetry Audit Stream")
st.dataframe(df_vis.sort_values(by='timestamp', ascending=False), use_container_width=True)
