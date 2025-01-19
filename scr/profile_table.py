from st_aggrid import GridOptionsBuilder, AgGrid
import streamlit as st

def display_aggrid_table(profile_user, editable):
    profile = profile_user.copy() if editable else  profile_user[profile_user['Applied?'] == True].copy()

    list_level = ['Basic', 'Intermediate', 'Advanced','Expert']
    profile = profile[['index','Department','Year','Function','Description','Applied?','Level']]

    grid_options_builder = GridOptionsBuilder.from_dataframe(profile)
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
        profile,
        gridOptions=grid_options,
        height=600,
        fit_columns_on_grid_load=True,
        theme="balham")
    selected_functions = selected_functions['data']

    return selected_functions
