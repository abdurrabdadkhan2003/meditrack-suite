import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Operational Analytics", page_icon="📊", layout="wide")

# Security check: Kick user out if not authenticated
if 'api' not in st.session_state or not st.session_state.api.token:
    st.warning("⚠️ Authentication required. Please log in from the main page.")
    st.stop()

api = st.session_state.api

st.title("📊 Operational Analytics & Footfall")
st.markdown("Real-time clinic utilization metrics directly from the Meditrack database.")

with st.spinner("Compiling operational data..."):
    patients = api.get_patients()
    appointments = api.get_appointments()

if not appointments:
    st.info("No appointment data available for visualization.")
    st.stop()

# Load into Pandas
df_appts = pd.DataFrame(appointments)
df_appts['scheduled_time'] = pd.to_datetime(df_appts['scheduled_time'])
df_appts['date_only'] = df_appts['scheduled_time'].dt.date

# Row 1: KPI Metrics
total_appts = len(df_appts)
completed = len(df_appts[df_appts['status'] == 'COMPLETED'])
no_shows = len(df_appts[df_appts['status'] == 'NO_SHOW'])
completion_rate = (completed / total_appts) * 100 if total_appts > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Bookings", total_appts)
col2.metric("Completed Consultations", completed)
col3.metric("No-Shows", no_shows)
col4.metric("Completion Rate", f"{completion_rate:.1f}%")

st.markdown("---")

# Row 2: Charts
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("7-Day Appointment Volume")
    daily_counts = df_appts.groupby('date_only').size().reset_index(name='count')
    daily_counts = daily_counts.sort_values('date_only').tail(7)

    fig_line = px.line(
        daily_counts,
        x='date_only',
        y='count',
        markers=True,
        labels={'date_only': 'Date', 'count': 'Appointments'},
        template="plotly_white"
    )
    st.plotly_chart(fig_line, use_container_width=True)

with chart_col2:
    st.subheader("Appointment Status Distribution")
    status_counts = df_appts['status'].value_counts().reset_index()
    status_counts.columns = ['status', 'count']

    fig_pie = px.pie(
        status_counts,
        names='status',
        values='count',
        hole=0.4,
        color='status',
        color_discrete_map={
            'COMPLETED': '#2e7b32',
            'SCHEDULED': '#1976d2',
            'NO_SHOW': '#d32f2f',
            'CANCELLED': '#ed6c02'
        }
    )
    st.plotly_chart(fig_pie, use_container_width=True)
