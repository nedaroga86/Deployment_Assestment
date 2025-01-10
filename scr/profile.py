import numpy as np
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid

from conf_page import set_config_page
from load_files import load_files
from save_pickles import saving_profile


def mode_edition():
    st.session_state.mode = False

def run_assessment(function):
    if 'mode' not in st.session_state:
        st.session_state.mode = False
    set_config_page()
    year = st.sidebar.selectbox('Year', options=[2024,2025])

    if st.session_state.profile == 'auto':
        selected_employee = st.session_state.name
    else:
        employees = st.session_state.team
        selected_employee = st.sidebar.selectbox('Employee', options=employees)


    st. subheader(f'Profile of "{selected_employee}"')
    function = function[(function['Department']== st.session_state.area)]
    function = read_saved_profile_user(function, selected_employee)
    # function = function[(function['Year']== year)]

    if st.session_state.mode == False and st.session_state.profile == 'team':
        if st.button('Active Edition'):
            st.session_state.mode  = True
            st.rerun()

    if st.session_state.mode:
        st.text('Editting Functions')
        year = st.selectbox('year', options=[2024,2025,2026])
        function['Year'] = year
        selected_functions = display_aggrid_table(function, True)
        if st.button('Update Profile'):
            saving_profile(selected_employee, selected_functions)
            st.session_state.mode = False
            st.rerun()
    else:
        st.text('Current Active Functions')
        selected_functions = display_aggrid_table(function[function['Applied?']==True], False)
        selected_functions = selected_functions['data']
        selected_functions = selected_functions[selected_functions['Applied?']==True]
        selected_functions['Employee Name'] = selected_employee
        selected_functions['Level'] = 'Basic'


def read_saved_profile_user(function, selected_employee):
    try:
        function = function.reset_index()
        files = load_files()
        profile_user = files.get_profile(selected_employee)
        function[['Year','Applied?', 'Level', 'Own']] = function.merge(
            profile_user,
            how='left',
            left_on='index',
            right_on='index'
        )[['Year','Applied?','Level','Own']]
        function['Applied?'] = np.where(function['Applied?'].isna(), False, function['Applied?'])
        function['Level'] = np.where(function['Level'].isna(), 'Basic', function['Level'])
    except:
        function['Applied?'] = False
        function['Level'] = 'Basic'
        function['Year'] = 0
        function['Own'] = 0
    return function


def display_aggrid_table(function, editable):

    list_level = ['Basic', 'Intermediate', 'Advanced','Expert']
    function = function[['index','Department','Year','Function','Description','Applied?','Level']]
    grid_options_builder = GridOptionsBuilder.from_dataframe(function)
    grid_options_builder.configure_default_column(resizable=True, autoSizeColumns=True, wrapText = True)
    grid_options_builder.configure_column("index",  hide=True)
    grid_options_builder.configure_column("Department", width=100)
    grid_options_builder.configure_column("Year", width=50)
    grid_options_builder.configure_column("Level", editable=editable, cellEditor='agSelectCellEditor',
                                          tooltipField="Function",
                                          cellEditorParams={'values': list_level},
                                          width=50)

    grid_options_builder.configure_column("Applied?", editable=editable,  sort="desc", width=80)
    grid_options_builder.configure_column("Description", wrapText=True, autoHeight=True)
    grid_options_builder.configure_grid_options(domLayout='normal',
                                                suppressHorizontalScroll=True,
                                                enableBrowserTooltips= True)
    grid_options = grid_options_builder.build()
    selected_functions = AgGrid(
        function,
        gridOptions=grid_options,
        height=600,
        fit_columns_on_grid_load=True,
        theme="balham")
    return selected_functions
