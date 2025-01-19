import os
import sqlite3

import streamlit as st
from streamlit_space import space

from conf_page import set_config_page
from manager_pickles import saving_profile,read_pickle_profile_user
from profile_table import display_aggrid_table
from filters import show_filter_menu
from buttons_design import new_button, eliminate_button


def mode_edition():
    st.session_state.mode = False
    st.session_state.mode_stake_holder = False

def get_profile_team(functions):
    set_config_page()
    if st.session_state.is_leader:
        if 'mode' not in st.session_state:
            st.session_state.mode = False
        if 'mode_stake_holder' not in st.session_state:
            st.session_state.mode_stake_holder = False
        year = show_filter_menu()

        employees = st.session_state.team
        selected_employee = st.sidebar.selectbox('Employee', options=employees)
        id_selected_employee = st.session_state.users_DB[st.session_state.users_DB['name']==selected_employee]['id'].iloc[0]

        profile_user = get_profile_user(functions, selected_employee, year)
        manage_profile_users(profile_user, selected_employee, year, id_selected_employee)
    else:
        st.subheader(f'Profile of employees on Charge')
        st.warning('You dont have persons on charge in our system.')



def manage_profile_users(profile_user, selected_employee, year,id_selected_employee):
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

        define_stake_holder(id_selected_employee, selected_employee, selected_functions, year)



def define_stake_holder(id_selected_employee, selected_employee, selected_functions, year):
    if not st.session_state.mode_stake_holder:
        id_stake_holder = st.session_state.users_DB[st.session_state.users_DB['id'] ==
                                                    id_selected_employee]['stakeholder'].iloc[0]
        sta, sta2,  = st.columns([2, 6])
        if id_stake_holder != '':

            stake_holder = st.session_state.users_DB[st.session_state.users_DB['id'] ==
                                                     id_stake_holder]['name'].iloc[0]
            sta.selectbox('Stakeholder',options=[f'{stake_holder}'], index=0, disabled=True)
        else:
            sta.selectbox('Stakeholder',options=['To assign an Stakeholder'], index=0, disabled=True)

        if st.button('Update Stakeholder'):
            st.session_state.mode_stake_holder = True
            st.rerun()
    else:
        sta, sta2 = st.columns([2, 6])
        sta.markdown('#### Stakeholder')
        stake_holder = sta.selectbox('Stakeholder',
                                     options=st.session_state.users_DB['name'],
                                     index=0,
                                     label_visibility="collapsed")

        stake_holder = st.session_state.users_DB[st.session_state.users_DB['name'] == stake_holder]['id'].iloc[0]
        space()
        with sta:
            opt, opt2 = st.columns([2, 2])
            with opt2:
                if new_button('Confirm'):
                    save_stakeholder(stake_holder, id_selected_employee)
                    st.session_state.mode_stake_holder = False
                    st.rerun()
            with opt:
                if eliminate_button('Cancel'):
                    st.session_state.mode_stake_holder = False
                    st.rerun()
        space(lines=2)



def get_profile_user(function, selected_employee, year):
    st.subheader(f'Profile of "{selected_employee}"')
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




