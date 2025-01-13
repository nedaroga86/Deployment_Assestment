
from st_aggrid import GridOptionsBuilder, AgGrid



def make_team_assessments(function):


    function = function[function['Applied?'] == True]
    function = function.melt(id_vars=['index', 'Department', "Year", 'Function', 'Description', 'Level','Own','Leader'],
                             value_vars=['Basic', 'Intermediate', 'Advanced', 'Expert'], var_name='Options',
                             value_name='Level Description')
    function = function[function['Options'] == function['Level']]

    function.drop(columns=['Options','Department'], inplace=True)
    function['Own'] = function.pop('Own')
    function['Leader'] = function.pop('Leader')
    grid_options_builder = GridOptionsBuilder.from_dataframe(function)
    grid_options_builder.configure_default_column(resizable=False, autoSizeColumns=True, multiSort=True)
    grid_options_builder.configure_column("index", hide=True)
    grid_options_builder.configure_column("Year", width=50)
    grid_options_builder.configure_column('Function', width=100)
    grid_options_builder.configure_column("Level", width=50)
    grid_options_builder.configure_column("Description", wrapText=True, autoHeight=True)
    grid_options_builder.configure_column("Level Description", wrapText=True, autoHeight=True)
    grid_options_builder.configure_column("Own", width=50)
    grid_options_builder.configure_column('Leader',
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
