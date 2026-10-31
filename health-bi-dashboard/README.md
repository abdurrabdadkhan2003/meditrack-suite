# health-bi-dashboard
Interactive Streamlit BI dashboard for Checklife operational and financial metrics.
# Checklife Health BI Dashboard (`health-bi-dashboard`)

Interactive Business Intelligence portal built with Streamlit, Pandas, and Plotly. Connects to the Meditrack Clinic Ops API via JWT authentication to visualize operational footfall, appointment utilization, and synthetic financial performance.

## Key Features
- **JWT Security Gateway**: Role-protected session state management.
- **Operational Analytics**: 7-day appointment trends and status breakdowns.
- **Financial Analytics**: Collected vs. outstanding revenue and claim rejection tracking.
- **Directory & Audit Exports**: Real-time search across patient records with one-click CSV downloads.

## Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py