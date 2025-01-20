import os
import sqlite3

import streamlit as st
from conf_page import set_config_page
from manager_pickles import read_pickle_profile_user
from profile_table import display_aggrid_table
from filters import show_filter_menu



def mode_edition():
    st.session_state.mode = False

def run_assessment(functions):
    if 'mode' not in st.session_state:
        st.session_state.mode = False
    set_config_page()
    year = show_filter_menu()

    selected_employee = st.session_state.name
    id_selected_employee = st.session_state.users_DB[st.session_state.users_DB['name']==selected_employee]['id'].iloc[0]

    st.subheader(f'This is your profile of {year}')
    profile_user = get_profile_user(functions, selected_employee, year)
    manage_profile_users(profile_user, selected_employee, id_selected_employee)


def manage_profile_users(profile_user, selected_employee,id_selected_employee):

    selected_functions = display_aggrid_table(profile_user, False)
    selected_functions = selected_functions[selected_functions['Applied?'] == True]
    if len(selected_functions)==0:
        st.warning("You don't have active functions for this period, if you need to activate some of them, "
                   "please reachout to leader.")
    selected_functions['Employee Name'] = selected_employee
    selected_functions['Level'] = 'Basic'

    id_stake_holder = st.session_state.users_DB[st.session_state.users_DB['id'] ==
                                                id_selected_employee]['stakeholder'].iloc[0]
    sta, sta2,  = st.columns([2, 6])
    if id_stake_holder != '':
        stake_holder = st.session_state.users_DB[st.session_state.users_DB['id'] ==
                                                 id_stake_holder]['name'].iloc[0]
        sta.selectbox('Stakeholder',options=[f'{stake_holder}'], index=0, disabled=True)
    else:
        sta.selectbox('Stakeholder',options=['To assign an Stakeholder'], index=0, disabled=True)


def get_profile_user(function, selected_employee, year):

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




