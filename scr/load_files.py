import os


import pandas as pd
import streamlit


class load_files:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def get_functions(self):
        db_path = os.path.join(self.BASE_DIR,'..', 'files', 'function.pickle')
        functions = pd.read_pickle(db_path)
        return functions

    def get_profile(self, employee):
        db_path = os.path.join(self.BASE_DIR,'..', 'profiles', f'{employee}_profile.pickle')
        try:
            profile_selected = pd.read_pickle(db_path)
        except:
            profile_selected = pd.DataFrame(columns=['index','Department','Function','Description','Applied?','Level','Year','Own','Leader','Stakeholer'])
            profile_selected.to_pickle(db_path)
            pass
        return profile_selected


