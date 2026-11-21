import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="System Health & Audit Trail", page_icon="🛡️", layout="wide")

if 'api' not in st.session_state or not st.session_state.api.token:
    st.warning("⚠️ Authentication required. Please log in from the main page.")
    st.stop()

api = st.session_state.api

st.title("🛡️ System Health & Role-Based Security Audit Trail")
st.markdown("Real-time infrastructure telemetry, API latency monitoring, and immutable compliance audit logs.")

with st.spinner("Polling infrastructure health and security logs..."):
    health = api.get_system_health()
    audit_logs = api.get_audit_logs()

df_audit = pd.DataFrame(audit_logs)

# --- Row 1: Infrastructure Health KPIs ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("FastAPI Backend Status", health["api_status"])
col2.metric("Database Engine", health["db_status"])
col3.metric("API Round-Trip Latency", f"{health['latency_ms']} ms")
col4.metric("30-Day System Uptime", f"{health['uptime_pct']}%")

st.markdown("---")

# --- Row 2: Security Audit Visualizations ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("Audit Events by RBAC Role")
    role_counts = df_audit['role'].value_counts().reset_index()
    role_counts.columns = ['role', 'count']
    fig_roles = px.pie(
        role_counts,
        names='role',
        values='count',
        hole=0.45,
        color='role',
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    st.plotly_chart(fig_roles, use_container_width=True)

with c2:
    st.subheader("Activity Frequency by Event Type")
    action_counts = df_audit['action'].value_counts().reset_index()
    action_counts.columns = ['action', 'count']
    fig_actions = px.bar(
        action_counts,
        x='count',
        y='action',
        orientation='h',
        labels={'count': 'Event Count', 'action': 'Action Code'},
        template="plotly_white",
        color_discrete_sequence=['#2e7b32']
    )
    st.plotly_chart(fig_actions, use_container_width=True)

st.markdown("---")

# --- Row 3: Filterable Security Audit Table ---
st.subheader("🔍 Immutable Security & Compliance Event Log")

f_col1, f_col2 = st.columns(2)
with f_col1:
    selected_roles = st.multiselect(
        "Filter by RBAC Role",
        options=df_audit['role'].unique().tolist(),
        default=df_audit['role'].unique().tolist()
    )
with f_col2:
    selected_actions = st.multiselect(
        "Filter by Action Code",
        options=df_audit['action'].unique().tolist(),
        default=df_audit['action'].unique().tolist()
    )

filtered_audit = df_audit[
    (df_audit['role'].isin(selected_roles)) &
    (df_audit['action'].isin(selected_actions))
]

st.dataframe(filtered_audit, use_container_width=True)

csv_audit = filtered_audit.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Export Filtered Security Audit Log (CSV)",
    data=csv_audit,
    file_name="meditrack_security_audit_log.csv",
    mime="text/csv",
    use_container_width=True
)
