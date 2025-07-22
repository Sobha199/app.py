
# Streamlit version of the 3-page login and dashboard application
import streamlit as st
import pandas as pd
from datetime import date

# Simulated employee data
EMPLOYEE_DATA = {
    "1001": {"name": "John Doe", "team_lead": "Alice Smith"},
    "1002": {"name": "Jane Smith", "team_lead": "Bob Brown"}
}

PROJECTS = ["Elevance MA", "Elevance ACA", "Health OS"]
CATEGORIES = ["Entry", "Recheck", "QA"]
LOGIN_NAMES = ["login1", "login2", "login3"]

# Session state for login and submitted data
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'emp_id' not in st.session_state:
    st.session_state.emp_id = ""
if 'submitted_data' not in st.session_state:
    st.session_state.submitted_data = []

# Page 1: Login
if not st.session_state.logged_in:
    st.image("s2m-logo.png", width=120)
    st.markdown("## Login Portal")
    username = st.text_input("Username", key="username", help="Enter your username")
    password = st.text_input("Password", type="password", key="password", help="Enter your password")

    if st.button("Sign In"):
        with st.spinner("Loading..."):
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.session_state.emp_id = username
            st.experimental_rerun()

# Page 2: Data Entry
elif st.session_state.logged_in and not st.session_state.get("view_dashboard", False):
    st.title("Data Entry Form")

    today = date.today()
    emp_id = st.session_state.emp_id
    emp_info = EMPLOYEE_DATA.get(emp_id, {})

    with st.form("entry_form"):
        col1, col2 = st.columns(2)
        with col1:
            date_field = st.date_input("Date", today)
            emp_id_input = st.text_input("Emp ID", value=emp_id, disabled=True)
            emp_name = st.text_input("Emp Name", value=emp_info.get("name", ""), disabled=True)
            project = st.selectbox("Project", PROJECTS)
            project_cat = st.selectbox("Project Category", CATEGORIES)
            login_name = st.selectbox("Login Name", LOGIN_NAMES)
            login_id = st.text_input("Login ID", value=login_name, disabled=True)

        with col2:
            team_lead = st.text_input("Team Lead Name", value=emp_info.get("team_lead", ""), disabled=True)
            chart_id = st.text_input("Chart ID")
            page_no = st.text_input("Page No")
            no_of_dos = st.number_input("No of DOS", min_value=0)
            no_of_codes = st.number_input("No of Codes", min_value=0)
            error_type = st.text_input("Error Type")
            error_comments = st.text_area("Error Comments")
            no_of_errors = st.number_input("No of Errors", min_value=0)
            chart_status = st.text_input("Chart Status")
            auditor_emp_id = st.text_input("Auditor Emp ID")
            auditor_name = st.text_input("Auditor Emp Name")

        submitted = st.form_submit_button("Submit")

        if submitted:
            data = {
                "Date": date_field,
                "Emp ID": emp_id,
                "Emp Name": emp_info.get("name", ""),
                "Project": project,
                "Category": project_cat,
                "Login Name": login_name,
                "Login ID": login_name,
                "Team Lead": emp_info.get("team_lead", ""),
                "Chart ID": chart_id,
                "Page No": page_no,
                "No of DOS": no_of_dos,
                "No of Codes": no_of_codes,
                "Error Type": error_type,
                "Error Comments": error_comments,
                "No of Errors": no_of_errors,
                "Chart Status": chart_status,
                "Auditor Emp ID": auditor_emp_id,
                "Auditor Name": auditor_name,
            }
            st.session_state.submitted_data.append(data)
            st.session_state.view_dashboard = True
            st.success("Data submitted successfully!")
            st.experimental_rerun()

# Page 3: Dashboard
elif st.session_state.logged_in and st.session_state.get("view_dashboard", False):
    st.title("Dashboard")
    df = pd.DataFrame(st.session_state.submitted_data)
    st.dataframe(df)

    if not df.empty:
        total_logins = len(df)
        total_dos = df["No of DOS"].sum()
        total_charts = df["Chart ID"].count()
        total_codes = df["No of Codes"].sum()
        working_days = df["Date"].nunique()
        cph = (total_charts / working_days) if working_days else 0

        st.metric("Total No of Logins", total_logins)
        st.metric("No of HC (assumed charts)", total_charts)
        st.metric("No of Working Days", working_days)
        st.metric("No of Charts", total_charts)
        st.metric("No of DOS", total_dos)
        st.metric("No of ICD (Codes)", total_codes)
        st.metric("CPH (Charts per Day)", round(cph, 2))

    st.button("Back to Form", on_click=lambda: st.session_state.update({"view_dashboard": False}))
