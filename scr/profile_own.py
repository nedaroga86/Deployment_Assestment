import streamlit as st
from conf_page import set_config_page
from manager_pickles import read_pickle_profile_user
from profile_table import display_aggrid_table





def run_assessment(functions, year, selected_employee):
    if 'mode' not in st.session_state:
        st.session_state.mode = False
    set_config_page()

    st.subheader(f'Functions of {selected_employee} - {year}')
    profile_user = get_profile_user(functions, selected_employee, year)
    manage_profile_users(profile_user, selected_employee)


def manage_profile_users(profile_user, selected_employee):

    selected_functions = display_aggrid_table(profile_user, False)
    selected_functions = selected_functions[selected_functions['Applied?'] == True]
    if len(selected_functions)==0:
        st.warning("You don't have active functions for this period, if you need to activate some of them, "
                   "please reachout to leader.")
    selected_functions['Employee Name'] = selected_employee
    selected_functions['Level'] = 'Basic'




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


