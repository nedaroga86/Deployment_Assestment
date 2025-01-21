import time

import streamlit as st

from conf_page import set_config_page
from manager_pickles import read_pickle_profile_user, update_scores
from buttons_design import new_button, eliminate_button
from assesment_Own_Scores import make_own_assesssments
from assessment_Leader_Scores import show_team_assessments
from filters import show_filter_menu


def get_score(function,selected_employee, year):
    set_config_page()
    profile = st.session_state.profile_selected
    if st.session_state.mode == False and profile == 'Leader Profile':
        if 'cancel' in st.session_state:
            st.text('')
            del st.session_state['cancel']
            st.rerun()

        make_team_assessment(function,selected_employee,year)
    else:
        if 'cancel' in st.session_state:
            st.text('')
            del st.session_state['cancel']
            st.rerun()
        st.subheader(f'My Assessment for {year}')
        make_individual_assessment(function,year)




def process_new_scores(scores, selected_employee, score):
    done = scores['data'][score].min() != 0 and scores['data'].empty == False
    if done:
        st.info("All Functions are complete, after saved you won't able to edit the scores")
    col, col2, col3 = st.columns([2, 4, 2])
    with col:
        cancel = eliminate_button('Cancel')
    if done:
        with col3:
            save = new_button('Save')
            if save:
                update_scores(selected_employee, scores,score)
                time.sleep(1)
                st.rerun()
    if cancel:
        st.session_state.cancel = True
        st.rerun()


def make_team_assessment(function,selected_employee,year):
    st.subheader(f'Assessment {selected_employee} for {year}')
    function = function[function['Department'] == st.session_state.area]
    function = read_pickle_profile_user(function, selected_employee,year)
    function = function[function['Applied?'] == True]
    function = function[function['Year'] == year]
    employee_score =  function['Own'].min() != 0 and function.empty == False
    if employee_score:
        scores = show_team_assessments(function)
        process_new_scores(scores, selected_employee,'Leader')
    else:
        st.warning(f'Please, reach out to {selected_employee} to complete the their assessment for year {year}')



def make_individual_assessment(function,year):
    selected_employee = st.session_state.name
    function = function[function['Department'] == st.session_state.area]
    function = read_pickle_profile_user(function, selected_employee,year)
    scores = make_own_assesssments(function, year)
    process_new_scores(scores, selected_employee, 'Own')