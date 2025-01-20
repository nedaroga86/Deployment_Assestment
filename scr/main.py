import streamlit as st
from profile_own import run_assessment
from load_files import load_files
from assessment_process import get_score
from profile_team import get_profile_team
from admin_site import Setup
from reports import Reports
from buttons_design import eliminate_button
from hardskills import Hardskills_class
from softskills import Softskills_class


class Main_Program:
    def __init__(self):
        self.jobs = 0

    def get_start(self):


        menu_options = ["Functions","Softskills","Hardskills","Assessments", 'Reports','Setup']
        with st.sidebar:
            logout =eliminate_button('Logout')
            if logout:
                if st.session_state.logged_in:
                    st.session_state.logged_in = False
                st.rerun()



        page = st.sidebar.selectbox("Sections:", options=menu_options)

        if page == "Functions":
            sub_menu_options = ["Your Functions","Team Functions"]
            sub_page = st.sidebar.radio("Sections:", options=sub_menu_options)
        elif page == "Assessments":
            options =['As Employee']
            options.append('As Leader') if st.session_state.is_leader else options
            options.append('As Stakeholder') if st.session_state.is_stakeholder else options
            asset = st.sidebar.radio("Evaluator Profile:", options=options)
            sub_page = page
        else:
            sub_page = page


        st.sidebar.divider()

        files = load_files()
        function = files.get_functions()


        if sub_page == "Your Functions":
            run_assessment(function)
        elif sub_page =="Team Functions":
            get_profile_team(function)
        elif sub_page == 'Assessments':
            get_score(function, asset)
        elif sub_page == "Reports":
            reports = Reports()
            reports.get_reports()
        elif sub_page == "Softskills":
            soft = Softskills_class()
            soft.get_softskills()
        elif sub_page == "Hardskills":
            hard = Hardskills_class()
            hard.get_hardskills()
        elif sub_page == "Setup":
            admin = Setup()
            admin.setup()

