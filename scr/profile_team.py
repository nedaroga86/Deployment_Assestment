import os
import sqlite3

import streamlit as st
from streamlit_space import space

from conf_page import set_config_page
from manager_pickles import saving_profile,read_pickle_profile_user
from profile_table import display_aggrid_table
from buttons_design import new_button, eliminate_button



def get_profile_team(functions, year, selected_employee):
    set_config_page()
    if st.session_state.is_leader:
        if 'mode' not in st.session_state:
            st.session_state.mode = False
        if 'mode_stake_holder' not in st.session_state:
            st.session_state.mode_stake_holder = False

        profile_user = get_profile_user(functions, selected_employee, year)
        manage_profile_users(profile_user, selected_employee, year)
    else:
        st.subheader(f'Profile of employees on Charge')
        st.warning('You dont have persons on charge in our system.')



def manage_profile_users(profile_user, selected_employee, year):
    if st.session_state.mode == False:
        if st.button(f'Edit Functions period {year}'):
            st.session_state.mode = True
            st.rerun()
    if st.session_state.mode:
        st.text(f'Editting Functions of period {year}')
        selected_functions = display_aggrid_table(profile_user, True)
        col, col2, col3 = st.columns([2, 4, 2])

        with col3:
            space()
            if new_button('Update Profile'):
                saving_profile(selected_employee, selected_functions, year)
                st.session_state.mode = False
                st.rerun()
        with col:
            if eliminate_button('Cancel'):
                st.session_state.mode = False
                st.rerun()

    else:
        st.text('Current Active Functions')
        selected_functions = display_aggrid_table(profile_user, False)
        selected_functions = selected_functions[selected_functions['Applied?'] == True]
        selected_functions['Employee Name'] = selected_employee
        selected_functions['Level'] = 'Basic'


def get_profile_user(function, selected_employee, year):
    st.subheader(f'Functions of "{selected_employee}"')
    function = function[(function['Department'] == st.session_state.area)]
    profile_user = read_pickle_profile_user(function, selected_employee, year)
    if year in profile_user['Year'].values:
        profile_user = profile_user[(profile_user['Year'] == year)]
    else:
        profile_user['Applied?'] = False
        profile_user['Level'] = 'Basic'
        profile_user['Year'] = year
        profile_user['Own'] = 0
        profile_user['Leader'] = 0
        profile_user['Stakeholer'] = 0
    return profile_user


def save_stakeholder(id_stake_holder,id_selected_employee):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, '..', 'dataBase', 'users.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("UPDATE users_table SET stakeholder = ? WHERE id = ?", (id_stake_holder, id_selected_employee))
    conn.commit()
    conn.close()




