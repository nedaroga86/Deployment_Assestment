import streamlit as st
from conf_page import set_config_page
from manager_pickles import read_pickle_softskills_user
from profile_table import display_soft_skills_aggrid_table


class Softskills_class:

    def get_softskills(self,soft_skills, year, selected_employee):
        if 'mode' not in st.session_state:
            st.session_state.mode = False
        set_config_page()
        st.subheader(f'Soft Skills of {selected_employee} - {year}')
        soft_skills_user = self.get_profile_user(soft_skills, selected_employee, year)
        manage_profile_users(soft_skills_user, selected_employee)



    def get_profile_user(self, soft_skills, selected_employee, year):
        profile_user = read_pickle_softskills_user(soft_skills, selected_employee, year)
        if year in profile_user['Year'].values:
            profile_user = profile_user[(profile_user['Year'] == year)]
        else:
            profile_user['Applied?'] = False
            profile_user['Level'] = 'Basic'
            profile_user['Year'] = year
            profile_user['Leader' ] = 0
        return profile_user


def manage_profile_users(soft_skills, selected_employee):

    selected_functions = display_soft_skills_aggrid_table(soft_skills, False)
    selected_functions = selected_functions[selected_functions['Applied?'] == True]
    if len(selected_functions)==0:
        st.warning("You don't have active functions for this period, if you need to activate some of them, "
                   "please reachout to leader.")
    selected_functions['Employee Name'] = selected_employee
    selected_functions['Level'] = 'Basic'