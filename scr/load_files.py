import os
import pandas as pd

class load_files:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def get_functions(self):
        db_path = os.path.join(self.BASE_DIR,'..', 'files', 'function.pickle')
        functions = pd.read_pickle(db_path)
        return functions

    def get_softskills(self):
        db_path = os.path.join(self.BASE_DIR,'..', 'files', 'softSkills.pickle')
        softskills = pd.read_pickle(db_path)
        return softskills

    def get_hardskills(self):
        db_path = os.path.join(self.BASE_DIR,'..', 'files', 'hardSkills.pickle')
        hardskills = pd.read_pickle(db_path)
        return hardskills

    def get_funcions_per_user(self, employee):
        db_path = os.path.join(self.BASE_DIR,'..', 'profiles_functions', f'{employee}_profile.pickle')
        try:
            profile_selected = pd.read_pickle(db_path)
        except:
            profile_selected = pd.DataFrame(columns=['index','Department','Function','Description','Applied?','Level','Year','Own','Leader','Stakeholer'])
            profile_selected.to_pickle(db_path)
            pass
        return profile_selected

    def get_softskills_per_user(self, employee):
        db_path = os.path.join(self.BASE_DIR,'..', 'profiles_softskills', f'{employee}_softskills.pickle')
        try:
            profile_selected = pd.read_pickle(db_path)
        except:
            profile_selected = pd.DataFrame(columns=['index','Softskills','Description','Applied?','Level','Year','Leader'])
            profile_selected.to_pickle(db_path)
            pass
        return profile_selected

    def get_hardskills_per_user(self, employee):
        db_path = os.path.join(self.BASE_DIR,'..', 'profiles_hardskills', f'{employee}_hardskills.pickle')
        try:
            profile_selected = pd.read_pickle(db_path)
        except:
            profile_selected = pd.DataFrame(columns=['index','Competency','Competency Description','Applied?','Level','Year','Leader'])
            profile_selected.to_pickle(db_path)
            pass
        return profile_selected