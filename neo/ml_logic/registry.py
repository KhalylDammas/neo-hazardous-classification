import os
import pickle
import datetime
import pandas as pd

from pathlib import Path
from neo.params import *


def model_save(model:object, file_name:str=None) -> None:
    '''
    Saves the model as `.pkl`.
    ####
    Parameters:-
    - model:object -> The model to be saved.
    - file_name:str (None) -> set the file name. If `None` uses the current tame stamp as the files name (YYYY-mm-dd_HHMMSS.pkl)
    '''
    if file_name==None:
        format_time = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        file_name = f"{format_time}.pkl"

    elif file_name[-4:] !='.pkl':
        file_name = f"{file_name}.pkl"
    file_path = os.path.join(MODELS_PATH, file_name)
    with open(file_path, 'wb') as file:
        pickle.dump(model, file)


def model_load(file_name:str=None, most_recent:bool=True) -> None:
    '''
    Load the model from `models` directory.
    - `file_name`:str (None) -> loads the file with this specific name.
    - `most_recent`:bool (True) -> Overrides `file_name` and loads the most recent updated model.
    ###
    returns:-
        model:object -> Loaded model.
    '''
    if most_recent:
        pkl_files = [file for file in Path(MODELS_PATH).glob('.pkl')]

        sort_files = sorted(pkl_files, key=lambda x: os.path.getmtime(x), reverse=True)
        if sort_files:
            file_name = sort_files[0]
        else:
            print("Directory is Empty...\n")

    file_path = os.path.join(MODELS_PATH, file_name)
    with open(file_path, 'rb') as file:
        model = pickle.load(file)

    return model


def save_results(results:dict, model_name:str) -> None:

    file_path = os.path.join(os.path.join(MODELS_PATH, 'results'), f"{model_name}_results.csv")
    cols = list(results.keys())
    pd.DataFrame(
        results,
        columns=cols
    ).to_csv(file_path)
