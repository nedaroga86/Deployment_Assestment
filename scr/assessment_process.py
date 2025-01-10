import time

import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid

from conf_page import set_config_page
from profile import read_saved_profile_user
from buttons_design import new_button, eliminate_button
from save_pickles import update_own_score


def get_score(function):
    set_config_page()
    st.sidebar.subheader('Assesstment')

    if st.session_state.mode == False and st.session_state.profile == 'team':
        make_team_assessment(function)
    else:
        if 'cancel' in st.session_state:
            st.text('')
            del st.session_state['cancel']
            st.rerun()
        else:
            selected_employee = st.session_state.name
            function = function[function['Department'] == st.session_state.area]
            function = read_saved_profile_user(function, selected_employee)
            scores = make_own_assesssment_v2(function)
            done =  scores['data']['Own'].min() != 0 and scores['data'].empty == False
            if done:
                st.info("All Functions are complete, after saved you won't able to edit the scores")
            col, col2, col3 = st.columns([2,4,2])
            with col:
               cancel = eliminate_button('Cancel')
            if done:
                with col3:
                    save = new_button('Save')
                    if save:
                        update_own_score(selected_employee, scores)
                        time.sleep(1)
                        st.rerun()
            if cancel:
                st.session_state.cancel = True
                st.rerun()


def make_team_assessment(function):
    employees = st.session_state.team
    selected_employee = st.sidebar.selectbox('Employee', options=employees)
    if 'Your Score' in function:
        function = function[function['Department'] == st.session_state.area]
        function = read_saved_profile_user(function, selected_employee)
        function = function[function['Applied?'] == True]
        function = function.melt(id_vars=['index', 'Department', 'Year', 'Function', 'Description', 'Level'],
                                 value_vars=['Basic', 'Intermediate', 'Advanced', 'Expert'], var_name='Options',
                                 value_name='Level Description')
        function = function[function['Options'] == function['Level']]
        function['Leader Score'] = 0
        function.drop(columns=['Options'], inplace=True)
        no_edit = ['index', 'Department', 'Function', 'Description', 'Level', 'Level Description']
        st.data_editor(function, width=800, use_container_width=True, disabled=no_edit)
    else:
        st.warning(f'Please, reach out to {selected_employee} to complete the their assessment')



def make_own_assesssment_v2(function):

    year = st.sidebar.selectbox('Year Assessment', options=function['Year'].unique())
    function = function[function['Applied?'] == True]
    function = function.melt(id_vars=['index', 'Department', "Year", 'Function', 'Description', 'Level','Own'],
                             value_vars=['Basic', 'Intermediate', 'Advanced', 'Expert'], var_name='Options',
                             value_name='Level Description')
    function = function[function['Options'] == function['Level']]

    function.drop(columns=['Options','Department','Year'], inplace=True)
    function['Own'] = function.pop('Own')
    grid_options_builder = GridOptionsBuilder.from_dataframe(function)
    grid_options_builder.configure_default_column(resizable=False, autoSizeColumns=True, multiSort=True)
    grid_options_builder.configure_column("index", hide=True)
    grid_options_builder.configure_column('Function', width=100)
    grid_options_builder.configure_column("Level", width=50)
    grid_options_builder.configure_column("Description", wrapText=True, autoHeight=True)
    grid_options_builder.configure_column("Level Description", wrapText=True, autoHeight=True)
    grid_options_builder.configure_column("Own",
                                          editable=True,
                                          sort="desc",
                                          width=50,
                                          type=["numericColumn", "numberColumnFilter"],
                                          cellEditor="agSelectCellEditor",
                                          cellEditorParams={'values': [1,2,3,4,5]})
    grid_options_builder.configure_grid_options(
        suppressColumnVirtualisation=True,
        suppressHorizontalScroll=True,
    )
    grid_options_builder.configure_default_column(resizable=True, autoSizeColumns=True, wrapText = True)
    grid_options = grid_options_builder.build()
    selected_functions = AgGrid(
        function,
        gridOptions=grid_options,
        height=600,
        fit_columns_on_grid_load=True,
        theme="balham",
        )
    return selected_functions

