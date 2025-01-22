import streamlit as st
from streamlit_option_menu import option_menu

from profile_own import run_assessment
from load_files import load_files
from assessment_process import get_score
from admin_site import Setup
from reports import Reports
from buttons_design import eliminate_button
from hardskills import Hardskills_class
from filters import show_filter_menu
from profile_team import get_profile_team
from stakeholder_team import get_stakeholder_team
from softskills import Softskills_class


class Main_Program:
    def __init__(self):
        self.jobs = 0

    def get_start(self):
        if 'profile_selected' not in st.session_state:
            st.session_state.profile_selected = 'My Profile'

        menu_options = ["Categories","Assessments", 'Reports','Setup']
        col0, col1 = st.sidebar.columns([3,2])
        col0.subheader(st.session_state.profile_selected, divider=True)
        profile = col1.button('Change', use_container_width=True)
        st.sidebar.divider()

        if profile:
            self.get_profile()
        with st.sidebar:
            logout =eliminate_button('Logout')
            if logout:
                if st.session_state.logged_in:
                    st.session_state.logged_in = False
                st.rerun()

        with st.sidebar.container(border=True):

            page = st.selectbox("Sections:", options=menu_options)
            year = show_filter_menu()


        files = load_files()
        function = files.get_functions()


        if st.session_state.profile_selected == 'My Profile':
            selected_employee = st.session_state.name
        else:
            employees = st.session_state.team
            selected_employee = st.sidebar.selectbox('Employee', options=employees)

        if page == 'Categories' or page == 'Assessments':
            if page == 'Categories':
                option =['Functions','Softskills','Hardskills','Stakeholder']
                icon= ['house', 'cloud-upload', "list-task", 'gear']
            else:
                option =['Functions','Softskills','Hardskills']
                icon =['house', 'cloud-upload', "list-task"]

            tab = option_menu(None, option,
                              icons=icon,
                              menu_icon="cast", default_index=0, orientation="horizontal")

        if page == 'Categories':
            if tab =='Functions':
                if st.session_state.profile_selected == 'My Profile':
                    run_assessment(function,year, selected_employee)
                else:
                    get_profile_team(function, year, selected_employee)
            elif tab=='Softskills':
                soft = Softskills_class()
                soft.get_softskills()
            elif tab=='Hardskills':
                hard = Hardskills_class()
                hard.get_hardskills()
            elif tab=='Stakeholder':
                if st.session_state.profile_selected == 'My Profile':
                    get_stakeholder_team('Own',  selected_employee)
                else:
                    get_stakeholder_team('Team',selected_employee)

        elif page == 'Assessments':
            get_score(function, selected_employee, year)
        elif page == "Reports":
            reports = Reports()
            reports.get_reports()
        elif page == "Setup":
            admin = Setup()
            admin.setup()


    @st.dialog('Select View Mode:')
    def get_profile(self):
        with st.form("Select an Profile", clear_on_submit=True):
            st.text('The list of the profiles is related to the configuration. If you have persons on charge you will see "Leader Profile", or if you'
                    'have any employee assigned to you as Steakholder you will see the option "Stakeholder Profile".')
            options = []
            if st.session_state.profile_selected != 'My Profile':
                options.append('My Profile')
            if st.session_state.profile_selected != 'Leader View':
                options.append('Leader View') if st.session_state.is_leader else options
            if st.session_state.profile_selected != 'Stakeholder View':
                options.append('Stakeholder View') if st.session_state.is_stakeholder else options
            profile = st.selectbox("Role:", options=options,
                                   label_visibility="collapsed")
            but1,but2, but3 = st.columns([2,3,2])
            submitted = but3.form_submit_button("Update", use_container_width=True)
            cancel = but1.form_submit_button("Cancel", use_container_width=True)

            if submitted:
                st.session_state.profile_selected = profile
                st.rerun()

            if cancel:
                st.rerun()

