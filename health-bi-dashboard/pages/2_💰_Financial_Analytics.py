import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Financial Analytics", page_icon="💰", layout="wide")

if 'api' not in st.session_state or not st.session_state.api.token:
    st.warning("⚠️ Authentication required. Please log in from the main page.")
    st.stop()

api = st.session_state.api

st.title("💰 Financial & Billing Analytics")
st.markdown("Synthetic revenue performance, invoice tracking, and insurance claim adjudication metrics.")

with st.spinner("Loading financial records..."):
    invoices = api.get_invoices()
    claims = api.get_claims()

df_inv = pd.DataFrame(invoices)
df_claims = pd.DataFrame(claims)

df_inv['issued_date'] = pd.to_datetime(df_inv['issued_date'])
df_inv['month_year'] = df_inv['issued_date'].dt.strftime('%Y-%m')

# --- Row 1: Top-Level Financial KPIs ---
total_revenue = df_inv[df_inv['status'] == 'PAID']['amount'].sum()
pending_revenue = df_inv[df_inv['status'] == 'ISSUED']['amount'].sum()
approved_claims = len(df_claims[df_claims['status'] == 'APPROVED'])
rejected_claims = len(df_claims[df_claims['status'] == 'REJECTED'])
rejection_rate = (rejected_claims / len(df_claims)) * 100 if len(df_claims) > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Collected Revenue", f"${total_revenue:,.2f}")
col2.metric("Outstanding Invoices", f"${pending_revenue:,.2f}")
col3.metric("Approved Claims", approved_claims)
col4.metric("Claim Rejection Rate", f"{rejection_rate:.1f}%")

st.markdown("---")

# --- Row 2: Interactive Financial Charts ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("Monthly Revenue by Invoice Status")
    monthly_rev = df_inv.groupby(['month_year', 'status'])['amount'].sum().reset_index()
    fig_rev = px.bar(
        monthly_rev,
        x='month_year',
        y='amount',
        color='status',
        barmode='group',
        labels={'month_year': 'Month', 'amount': 'Amount ($)', 'status': 'Status'},
        color_discrete_map={'PAID': '#2e7b32', 'ISSUED': '#1976d2', 'CANCELLED': '#d32f2f'},
        template="plotly_white"
    )
    st.plotly_chart(fig_rev, use_container_width=True)

with c2:
    st.subheader("Insurance Claims by Billing Procedure Code")
    code_summary = df_claims.groupby(['claim_code', 'status'])['claim_amount'].sum().reset_index()
    fig_claims = px.bar(
        code_summary,
        x='claim_code',
        y='claim_amount',
        color='status',
        labels={'claim_code': 'Billing Code', 'claim_amount': 'Claim Value ($)'},
        template="plotly_white"
    )
    st.plotly_chart(fig_claims, use_container_width=True)

st.markdown("---")
st.subheader("Recent High-Value Invoices")
st.dataframe(
    df_inv.sort_values(by='amount', ascending=False).head(15),
    use_container_width=True
)
