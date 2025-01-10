import os

import numpy as np
import pandas as pd
import streamlit as st



def saving_profile(selected_employee, selected_functions):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(BASE_DIR, '..', 'profiles', f"{selected_employee}_profile.pickle")
    selected_functions = selected_functions['data']
    selected_functions['Own'] = 0
    selected_functions['Leader'] = 0
    selected_functions['Stakeholer'] = 0
    st.dataframe(selected_functions)
    selected_functions.to_pickle(filename)
    st.success('The profile created/updated')


def update_own_score(selected_employee,data):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(BASE_DIR, '..', 'profiles', f"{selected_employee}_profile.pickle")
    user_data = pd.read_pickle(filename)
    user_data.reset_index(inplace=True, drop=True)
    merged =  user_data.merge(data['data'],how='left',left_on ='index', right_on ='index',
                             suffixes=(False,"_new"))[['Own_new']]
    merged['Own_new'] = np.where(merged['Own_new'].isna(),0,merged['Own_new'])
    user_data['Own'] = merged['Own_new']
    user_data.to_pickle(filename)
    st.success('Scores Updated')

