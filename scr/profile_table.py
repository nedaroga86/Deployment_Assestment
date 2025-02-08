import time

from st_aggrid import GridOptionsBuilder, AgGrid


def display_aggrid_table(profile_user, editable):
    import streamlit as st
    with st.spinner():
        time.sleep(1)
    profile = profile_user.copy() if editable else  profile_user[profile_user['Applied?'] == True].copy()

    list_level = ['Basic', 'Intermediate', 'Advanced','Expert']
    profile = profile[['index','Department','Year','Function','Description','Level','Applied?']]

    grid_options_builder = GridOptionsBuilder.from_dataframe(profile)
    grid_options_builder.configure_default_column(resizable=True, autoSizeColumns=True, wrapText = True)
    grid_options_builder.configure_column("index",  hide=True)
    grid_options_builder.configure_column("Department", width=100)
    grid_options_builder.configure_column("Year", width=50)
    grid_options_builder.configure_column("Applied?", editable=editable,  sort="desc", width=60)
    grid_options_builder.configure_column("Level", editable=editable, cellEditor='agSelectCellEditor',
                                          tooltipField="Function",
                                          cellEditorParams={'values': list_level},
                                          width=80)


    grid_options_builder.configure_column("Description", wrapText=True, autoHeight=True)
    grid_options_builder.configure_grid_options(domLayout='normal',
                                                suppressHorizontalScroll=True,
                                                enableBrowserTooltips= True)
    grid_options = grid_options_builder.build()
    selected_functions = AgGrid(
        profile,
        gridOptions=grid_options,
        height=600,
        fit_columns_on_grid_load=True,
        theme="streamlit")
    selected_functions = selected_functions['data']

    return selected_functions

def display_soft_skills_aggrid_table(soft_skills, editable):

    profile = soft_skills.copy() if editable else  soft_skills[soft_skills['Applied?'] == True].copy()

    list_level = ['Basic', 'Intermediate', 'Advanced','Expert']
    profile = profile[['index','Year','Soft Skill','Description','Level','Applied?']]

    grid_options_builder = GridOptionsBuilder.from_dataframe(profile)
    grid_options_builder.configure_default_column(resizable=True, autoSizeColumns=True, wrapText = True)
    grid_options_builder.configure_column("index",  hide=True)
    grid_options_builder.configure_column("Year", width=50)
    grid_options_builder.configure_column("Applied?", editable=editable,  sort="desc", width=60)
    grid_options_builder.configure_column("Level", editable=editable, cellEditor='agSelectCellEditor',
                                          tooltipField="Function",
                                          cellEditorParams={'values': list_level},
                                          width=80)


    grid_options_builder.configure_column("Description", wrapText=True, autoHeight=True)
    grid_options_builder.configure_grid_options(domLayout='normal',
                                                suppressHorizontalScroll=True,
                                                enableBrowserTooltips= True)
    grid_options = grid_options_builder.build()
    selected_functions = AgGrid(
        profile,
        gridOptions=grid_options,
        height=600,
        fit_columns_on_grid_load=True,
        theme="streamlit")
    selected_functions = selected_functions['data']

    return selected_functions


def display_hard_skills_aggrid_table(hard_skills, editable):

    profile = hard_skills.copy() if editable else  hard_skills[hard_skills['Applied?'] == True].copy()

    list_level = ['Basic', 'Intermediate', 'Advanced','Expert']
    profile = profile[['index','Year','Competency','Competency Description','Level','Applied?']]

    grid_options_builder = GridOptionsBuilder.from_dataframe(profile)
    grid_options_builder.configure_default_column(resizable=True, autoSizeColumns=True, wrapText = True)
    grid_options_builder.configure_column("index",  hide=True)
    grid_options_builder.configure_column("Year", width=50)
    grid_options_builder.configure_column("Applied?", editable=editable,  sort="desc", width=60)
    grid_options_builder.configure_column("Level", editable=editable, cellEditor='agSelectCellEditor',
                                          tooltipField="Function",
                                          cellEditorParams={'values': list_level},
                                          width=80)


    grid_options_builder.configure_column("Competency Description", wrapText=True, autoHeight=True)
    grid_options_builder.configure_grid_options(domLayout='normal',
                                                suppressHorizontalScroll=True,
                                                enableBrowserTooltips= True)
    grid_options = grid_options_builder.build()
    selected_functions = AgGrid(
        profile,
        gridOptions=grid_options,
        height=600,
        fit_columns_on_grid_load=True,
        theme="streamlit")
    selected_functions = selected_functions['data']

    return selected_functions