import pandas as pd


file = pd.read_csv('HardSkills.csv')
file.to_pickle('hardSkills.pickle')