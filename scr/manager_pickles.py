import os

import numpy as np
import pandas as pd
import streamlit as st

from load_files import load_files


def saving_profile(selected_employee, selected_functions, year):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(BASE_DIR, '..', 'profiles_functions', f"{selected_employee}_profile.pickle")
    profile_df = pd.read_pickle(filename)
    selected_df = selected_functions.copy()
    selected_df['Own'] = 0
    selected_df['Leader'] = 0
    selected_df['Stakeholer'] = 0

    profile_df = profile_df[profile_df['Year']!=year]
    profile_df = pd.concat([profile_df, selected_df], ignore_index=True)
    profile_df.to_pickle(filename)
    st.success('The profile has been saved.')



def update_scores(selected_employee,data, score):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(BASE_DIR, '..', 'profiles_functions', f"{selected_employee}_profile.pickle")
    user_data = pd.read_pickle(filename)
    user_data.reset_index(inplace=True, drop=True)
    merged =  user_data.merge(data['data'],how='left',
                              left_on =['index', 'Year'],
                              right_on =['index', 'Year'],
                             suffixes=('',"_new"))

    merged[f'{score}_new'] = np.where(merged[f'{score}_new'].isna(),merged[f'{score}'],merged[f'{score}_new'])
    user_data[f'{score}'] = merged[f'{score}_new']
    user_data.to_pickle(filename)
    st.success('Scores Updated')


def read_pickle_profile_user(function, selected_employee,year):
    function = function.reset_index()
    files = load_files()
    profile_user = files.get_funcions_per_user(selected_employee)

    unique_years = list(profile_user['Year'].unique())
    if len(unique_years) == 0 :
        function_expanded = function.copy()
        function_expanded['Year'] = year
    else:
        function_expanded = pd.concat(
            [function.assign(Year=year) for year in unique_years],
            ignore_index=True
    )

    updated_columns = ['Year', 'Applied?', 'Level', 'Own', 'Leader', 'Stakeholer']
    function_expanded[updated_columns] = function_expanded.merge(
        profile_user,
        how='left',
        on=['index', 'Year']
    )[updated_columns]

    function_expanded['Applied?'] = np.where(function_expanded['Applied?'].isna(), False, function_expanded['Applied?'])
    function_expanded['Level'] = np.where(function_expanded['Level'].isna(), 'Basic', function_expanded['Level'])
    function_expanded['Own'] = np.where(function_expanded['Own'].isna(), 0, function_expanded['Own'])
    function_expanded['Leader'] = np.where(function_expanded['Leader'].isna(), 0, function_expanded['Leader'])
    function_expanded['Stakeholer'] = np.where(function_expanded['Stakeholer'].isna(), 0, function_expanded['Stakeholer'])

    return function_expanded


def read_pickle_softskills_user(soft_skills, selected_employee,year):
    function = soft_skills.reset_index()
    files = load_files()
    profile_user = files.get_softskills_per_user(selected_employee)

    unique_years = list(profile_user['Year'].unique())
    if len(unique_years) == 0 :
        function_expanded = function.copy()
        function_expanded['Year'] = year
    else:
        function_expanded = pd.concat(
            [function.assign(Year=year) for year in unique_years],
            ignore_index=True
        )

    updated_columns = ['Year', 'Applied?', 'Level', 'Leader']
    function_expanded[updated_columns] = function_expanded.merge(
        profile_user,
        how='left',
        on=['index', 'Year']
    )[updated_columns]

    function_expanded['Applied?'] = np.where(function_expanded['Applied?'].isna(), False, function_expanded['Applied?'])
    function_expanded['Level'] = np.where(function_expanded['Level'].isna(), 'Basic', function_expanded['Level'])
    function_expanded['Leader'] = np.where(function_expanded['Leader'].isna(), 0, function_expanded['Leader'])
    return function_expanded


def saving_soft_skills(selected_employee, selected_functions, year):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(BASE_DIR, '..', 'profiles_softskills', f"{selected_employee}_softskills.pickle")
    profile_df = pd.read_pickle(filename)
    selected_df = selected_functions.copy()
    selected_df['Leader'] = 0

    profile_df = profile_df[profile_df['Year']!=year]
    profile_df = pd.concat([profile_df, selected_df], ignore_index=True)
    profile_df.to_pickle(filename)
    st.success('The profile has been saved.')


def read_pickle_hardskills_user(hard_skills, selected_employee,year):
    function = hard_skills.reset_index()
    files = load_files()
    profile_user = files.get_hardskills_per_user(selected_employee)

    unique_years = list(profile_user['Year'].unique())
    if len(unique_years) == 0 :
        function_expanded = function.copy()
        function_expanded['Year'] = year
    else:
        function_expanded = pd.concat(
            [function.assign(Year=year) for year in unique_years],
            ignore_index=True
        )

    updated_columns = ['Year', 'Applied?', 'Level', 'Leader']
    function_expanded[updated_columns] = function_expanded.merge(
        profile_user,
        how='left',
        on=['index', 'Year']
    )[updated_columns]

    function_expanded['Applied?'] = np.where(function_expanded['Applied?'].isna(), False, function_expanded['Applied?'])
    function_expanded['Level'] = np.where(function_expanded['Level'].isna(), 'Basic', function_expanded['Level'])
    function_expanded['Leader'] = np.where(function_expanded['Leader'].isna(), 0, function_expanded['Leader'])
    return function_expanded


def saving_hard_skills(selected_employee, selected_functions, year):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(BASE_DIR, '..', 'profiles_hardskills', f"{selected_employee}_hardskills.pickle")
    profile_df = pd.read_pickle(filename)
    selected_df = selected_functions.copy()
    selected_df['Leader'] = 0

    profile_df = profile_df[profile_df['Year']!=year]
    profile_df = pd.concat([profile_df, selected_df], ignore_index=True)
    profile_df.to_pickle(filename)
    st.success('The profile has been saved.')