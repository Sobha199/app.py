import streamlit as st
import pandas as pd
import datetime

# Load CSV
csv_path = "Tracking.csv"
df = pd.read_csv(csv_path)

# App title and theme
st.set_page_config(page_title="S2M Portal", layout="wide")
st.markdown("""
    <style>
        body {
            background-color: #e6f2ff;
        }
        .title {
            color: #008CBA;
            font-size: 36px;
            font-weight: bold;
        }
        .black-border input {
            border: 2px solid black !important;
        }
    </style>
""", unsafe_allow_html=True)

# Session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'form_data' not in st.session_state:
    st.session_state.form_data = []
if 'dashboard' not in st.session_state:
    st.session_state.dashboard = False

# Page 1: Login
if not st.session_state.logged_in:
    st.markdown("<div class='title'>S2M Login Portal</div>", unsafe_allow_html=True)
    with st.form("login_form"):
        emp_id = st.text_input("Emp ID", key="emp_id", help="Enter your Emp ID")
        password = st.text_input("Password", type="password", key="password")
        submit = st.form_submit_button("Login")

    if submit:
        user = df[df['Emp Id'] == int(emp_id)] if emp_id.isdigit() else pd.DataFrame()
        if not user.empty and user.iloc[0]['Password'] == password:
            st.session_state.logged_in = True
            st.session_state.user_data = user.iloc[0]
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")

# Role-based access
elif st.session_state.logged_in:
    role = st.session_state.user_data['Role']

    if role.lower() == 'admin':
        st.title("Admin Dashboard")
        st.write("Welcome, Admin!")
        st.dataframe(df)
        st.button("Go to Entry Page", on_click=lambda: st.session_state.update({'dashboard': False}))

    elif role.lower() == 'audit' or role.lower() == 'coder':
        if not st.session_state.dashboard:
            st.title("Data Entry Portal")
            user = st.session_state.user_data

            with st.form("entry_form"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    date = st.date_input("Date", value=datetime.date.today())
                    emp_id = user['Emp Id']
                    st.text_input("Emp ID", value=emp_id, disabled=True)
                with col2:
                    emp_name = user['Emp Name']
                    st.text_input("Emp Name", value=emp_name, disabled=True)
                    project = st.selectbox("Project", ["Elevance MA", "Elevance ACA", "Health OS"])
                with col3:
                    category = st.selectbox("Project Category", ["Entry", "Recheck", "QA"])
                    login_names = df['Login Name'].unique().tolist()
                    login_selected = st.multiselect("Login Name", login_names)

                login_id = ", ".join(df[df['Login Name'].isin(login_selected)]['Login Id'])
                st.text_input("Login ID", value=login_id, disabled=True)

                team_lead = "Team Lead Name Placeholder"  # Can be inferred logic if available
                st.text_input("Team Lead Name", value=team_lead, disabled=True)

                chart_id = st.text_input("Chart ID")
                page_no = st.text_input("Page No")
                no_of_dos = st.number_input("No of DOS", min_value=0)
                no_of_codes = st.number_input("No of Codes", min_value=0)
                error_type = st.text_input("Error Type")
                error_comments = st.text_area("Error Comments")
                no_of_errors = st.number_input("No of Errors", min_value=0)
                chart_status = st.selectbox("Chart Status", ["Completed", "Pending", "In Review"])
                auditor_id = st.text_input("Auditor Emp ID")
                auditor_name = st.text_input("Auditor Emp Name")

                submit = st.form_submit_button("Submit")

                if submit:
                    st.success("Form submitted successfully!")
                    st.session_state.form_data.append({
                        "Date": date,
                        "Emp ID": emp_id,
                        "Emp Name": emp_name,
                        "Project": project,
                        "Project Category": category,
                        "Login Name": login_selected,
                        "Login ID": login_id,
                        "Team Lead Name": team_lead,
                        "Chart ID": chart_id,
                        "Page No": page_no,
                        "No of DOS": no_of_dos,
                        "No of Codes": no_of_codes,
                        "Error Type": error_type,
                        "Error Comments": error_comments,
                        "No of Errors": no_of_errors,
                        "Chart Status": chart_status,
                        "Auditor ID": auditor_id,
                        "Auditor Name": auditor_name,
                    })

            st.button("Go to Dashboard", on_click=lambda: st.session_state.update({'dashboard': True}))

        else:
            st.title("Dashboard")
            data = pd.DataFrame(st.session_state.form_data)
            if not data.empty:
                st.metric("Total Logins", len(data))
                st.metric("No of HC", data['Emp ID'].nunique())
                st.metric("No of Working Days", data['Date'].nunique())
                st.metric("No of Charts", data['Chart ID'].nunique())
                st.metric("No of DOS", data['No of DOS'].sum())
                st.metric("No of ICD", data['No of Codes'].sum())
                st.metric("CPH", round(data['No of Codes'].sum() / max(1, len(data)), 2))
                st.dataframe(data)
            else:
                st.info("No data submitted yet.")

    else:
        st.warning("Unauthorized role.")
