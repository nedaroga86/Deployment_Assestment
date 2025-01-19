import streamlit as st

from streamlit_option_menu import option_menu
from profile_own import run_assessment
from load_files import load_files
from assessment_process import get_score

from profile_team import get_profile_team
from admin_site import Setup
from reports import Reports


class Main_Program:
    def __init__(self):
        self.jobs = 0

    def get_start(self):


        menu_options = ["Your Functions","Team Functions","Assessments", 'Reports','Setup',"Logout"]

        page = st.sidebar.radio("Sections:", options=menu_options)
        st.sidebar.divider()

        files = load_files()
        function = files.get_functions()


        if page == "Your Functions":
            run_assessment(function)
        elif page =="Team Functions":
            get_profile_team(function)
        elif page == 'Assessments':
            get_score(function)
        elif page == "Reports":
            reports = Reports()
            reports.get_reports()
        elif page == "Setup":
            admin = Setup()
            admin.setup()
        elif page == "Logout":
            if st.session_state.logged_in:
                st.session_state.logged_in = False
                st.rerun()

