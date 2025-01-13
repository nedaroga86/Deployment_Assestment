import streamlit as st
from streamlit_space import space

from conf_page import set_config_page
from manager_pickles import saving_profile,read_pickle_profile_user
from profile_table import display_aggrid_table
from filters import show_filter_menu
from buttons_design import new_button, eliminate_button


def mode_edition():
    st.session_state.mode = False

def run_assessment(functions):
    if 'mode' not in st.session_state:
        st.session_state.mode = False
    set_config_page()
    year = show_filter_menu()

    if st.session_state.profile == 'auto':
        selected_employee = st.session_state.name
    else:
        employees = st.session_state.team
        selected_employee = st.sidebar.selectbox('Employee', options=employees)

    profile_user = get_profile_user(functions, selected_employee, year)
    manage_profile_users(profile_user, selected_employee, year)


def manage_profile_users(profile_user, selected_employee, year):
    if st.session_state.mode == False and st.session_state.profile == 'team':
        if st.button('Active Edition'):
            st.session_state.mode = True
            st.rerun()
    if st.session_state.mode:
        st.text('Editting Functions')
        selected_functions = display_aggrid_table(profile_user, True)
        sta, sta2,  = st.columns([2, 6])
        sta.markdown('#### Stakeholder')
        st.session_state.stake_holder = sta.selectbox('Stakeholder',
                                                      options=st.session_state.users_DB['name'],
                                                      index=0,
                                                      label_visibility="collapsed")
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
        if 'stake_holder' in st.session_state:
            st.markdown(f'#### Stakeholder: {st.session_state.stake_holder}')
        else:
            st.markdown(f'#### To define Stakeholder')


def get_profile_user(function, selected_employee, year):
    st.subheader(f'Profile of "{selected_employee}"')
    function = function[(function['Department'] == st.session_state.area)]
    profile_user = read_pickle_profile_user(function, selected_employee)
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


