import numpy as np
import pandas as pd

from neo.params import *

from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


from neo.ml_logic.data import  preprocessing, clean_data
from neo.ml_logic.model import train_model, evaluate_model
from neo.ml_logic.registry import mlflow_run, mlflow_transition_model
from neo.ml_logic.registry import load_model, save_model, save_results
# from neo.ml_logic.preprocessor import preprocess_features     # Not yet exists...


def preprocess():

    data = pd.read_csv(DATA_LOCAL_PATH)

    data = clean_data(data)

    data = preprocessing(data)

    return data


def train():
    # TODO
    data = pd.read_csv(DATA_LOCAL_PATH)

    val_results = train_model()
    return val_results

def evaluate():
    # TODO
    return #score

def predict(model, X_new):
    # TODO
    return #model.predict(X_new)



if __name__ == '__main__':

    # TODO
    preprocess()
    train()
    evaluate()

    # Predict on new data
    X_new = pd.DataFrame({
        'absolute_magnitude': [-73.950655],
        'estimated_diameter_min': [40.783282],
        'relative_velocity': [-73.984365],
        'miss_distance': [40.769802]
    })
    y_pred = predict(model, X_new)
    print(f'Predicted Fare: {y_pred[0]}')
