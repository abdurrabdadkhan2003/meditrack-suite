import streamlit as st
from api_client import MeditrackAPIClient

st.set_page_config(page_title="Meditrack BI | Login", page_icon="🏥", layout="centered")

if 'api' not in st.session_state:
    st.session_state.api = MeditrackAPIClient()

api = st.session_state.api

st.title("🏥 Checklife Health Care Services")
st.subheader("Business Intelligence Portal")
st.markdown("---")

if not api.token:
    st.info("System locked. Please provide administrative credentials.")
    with st.form("login_form"):
        username = st.text_input("Username", value="admin_user")
        password = st.text_input("Password", type="password", value="admin123")
        submitted = st.form_submit_button("Authenticate")

        if submitted:
            if api.login(username, password):
                st.success("Authentication successful. Navigation unlocked.")
                st.rerun()
            else:
                st.error("Invalid credentials. Access denied.")
else:
    st.success("✅ Secure connection established with Clinic Ops API.")
    st.write("Use the sidebar to navigate through the operational dashboards.")

    if st.button("Terminate Session"):
        api.token = None
        st.rerun()
