import streamlit as st
import pandas as pd

st.set_page_config(page_title="Patient Directory & Exports", page_icon="🗂️", layout="wide")

if 'api' not in st.session_state or not st.session_state.api.token:
    st.warning("⚠️ Authentication required. Please log in from the main page.")
    st.stop()

api = st.session_state.api

st.title("🗂️ Patient Directory & Audit Exports")
st.markdown("Searchable patient records and one-click CSV data exports for offline compliance reporting.")

with st.spinner("Fetching directory..."):
    patients = api.get_patients()
    appointments = api.get_appointments()
    invoices = api.get_invoices()

df_patients = pd.DataFrame(patients)
df_appts = pd.DataFrame(appointments)
df_inv = pd.DataFrame(invoices)

# --- Search & Filter Bar ---
search_col1, search_col2 = st.columns([3, 1])
with search_col1:
    search_query = st.text_input("🔍 Search Patient by First Name, Last Name, or Contact Number", "")

if search_query:
    mask = (
        df_patients['first_name'].str.contains(search_query, case=False, na=False) |
        df_patients['last_name'].str.contains(search_query, case=False, na=False) |
        df_patients['contact_number'].str.contains(search_query, case=False, na=False)
    )
    filtered_patients = df_patients[mask]
else:
    filtered_patients = df_patients

st.write(f"Showing **{len(filtered_patients)}** of **{len(df_patients)}** synthetic patient records.")
st.dataframe(filtered_patients, use_container_width=True)

st.markdown("---")
st.subheader("📥 Compliance & Audit CSV Exports")

exp_col1, exp_col2, exp_col3 = st.columns(3)

with exp_col1:
    csv_patients = filtered_patients.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Patient Directory (CSV)",
        data=csv_patients,
        file_name="meditrack_patients_export.csv",
        mime="text/csv",
        use_container_width=True
    )

with exp_col2:
    csv_appts = df_appts.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Appointments Log (CSV)",
        data=csv_appts,
        file_name="meditrack_appointments_export.csv",
        mime="text/csv",
        use_container_width=True
    )

with exp_col3:
    csv_inv = df_inv.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Billing Ledger (CSV)",
        data=csv_inv,
        file_name="meditrack_billing_export.csv",
        mime="text/csv",
        use_container_width=True
    )
