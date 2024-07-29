import pandas as pd
import os

def extract_names(file_path):
    names = []
    data = pd.read_csv(file_path)
    for name in data['Food']:
        names.append(name)
    return names

def __main__():
    names = extract_names(os.getenv('FOOD_DATA_PATH'))
    print(names) 