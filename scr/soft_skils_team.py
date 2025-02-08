import os
import sqlite3

import streamlit as st
from streamlit_space import space

from conf_page import set_config_page
from manager_pickles import saving_soft_skills, read_pickle_softskills_user
from profile_table import  display_soft_skills_aggrid_table
from buttons_design import new_button, eliminate_button



def get_soft_skills_team(soft_skills, year, selected_employee):
    set_config_page()
    if st.session_state.is_leader:
        if 'mode' not in st.session_state:
            st.session_state.mode = False
        if 'mode_stake_holder' not in st.session_state:
            st.session_state.mode_stake_holder = False

        profile_user = get_soft_skills_user(soft_skills, selected_employee, year)
        manage_profile_users(profile_user, selected_employee, year)
    else:
        st.subheader(f'Soft Skills of employees on Charge')
        st.warning('You dont have persons on charge in our system.')



def manage_profile_users(soft_skill_user, selected_employee, year):
    if st.session_state.mode == False:
        if st.button(f'Edit Soft Skills period {year}'):
            st.session_state.mode = True
            st.rerun()
    if st.session_state.mode:
        st.text(f'Editting Soft Skills of period {year}')
        selected_functions = display_soft_skills_aggrid_table(soft_skill_user, True)
        col, col2, col3 = st.columns([2, 4, 2])

        with col3:
            space()
            if new_button('Update Sof Skills'):
                saving_soft_skills(selected_employee, selected_functions, year)
                st.session_state.mode = False
                st.rerun()
        with col:
            if eliminate_button('Cancel'):
                st.session_state.mode = False
                st.rerun()

    else:
        st.text('Current Active Soft Skills')
        selected_functions = display_soft_skills_aggrid_table(soft_skill_user, False)
        selected_functions = selected_functions[selected_functions['Applied?'] == True]
        selected_functions['Employee Name'] = selected_employee
        selected_functions['Level'] = 'Basic'


def get_soft_skills_user(soft_skill_user, selected_employee, year):
    st.subheader(f'Soft Skills of "{selected_employee}"')
    profile_user = read_pickle_softskills_user(soft_skill_user, selected_employee, year)
    if year in profile_user['Year'].values:
        profile_user = profile_user[(profile_user['Year'] == year)]
    else:
        profile_user['Applied?'] = False
        profile_user['Level'] = 'Basic'
        profile_user['Year'] = year
    return profile_user






