import streamlit as st

from streamlit_option_menu import option_menu
from profile import run_assessment
from load_files import load_files
from assessment_process import get_score
from setup import manage_setup


class Main_Program:
    def __init__(self):
        self.jobs = 0

    def get_start(self):

        if st.session_state.profile == 'auto':
            menu_options = ["Your Functions","Assessments", 'Reports','Setup',"Logout"]
        else:
            menu_options = ["Team Functions","Assessments", 'Reports','Setup',"Logout"]

        menu_styles = {
            "container": {"padding": "2px"},
            "nav-link": {
                "font-size": "14px",

                "text-align": "center",
                "margin": "5px",
                "hover-color": "#fafafa",
                "icon": {"color": "red"}
            },
            "nav-link-selected": {"background-color": "#ED2E17", "color": "white"}, #9E3E4A
            "icon": {"color": "#F0F0F0"},
            "nav-link-logout": {"color": "red", "hover-color": "#ffcccc"},
        }

        page = option_menu(None, menu_options,
                           icons=['bi bi-list-task','bi bi-table','bi bi-table'],
                           menu_icon="cast", default_index=0, orientation="horizontal",
                           styles=menu_styles)
        files = load_files()
        function = files.get_functions()


        if page == "Your Functions" or page =="Team Functions":
            run_assessment(function)
        if page == 'Assessments':
            get_score(function)
        elif page == "Reports":
            st.session_state.mode = False
        elif page == "Setup":
            manage_setup()
        elif page == "Logout":
            if st.session_state.logged_in:
                st.session_state.logged_in = False
                st.rerun()
