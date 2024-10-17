import numpy as np
import pandas as pd

from neo.params import *

from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


from neo.ml_logic.data import  preprocessing, clean_data
from neo.ml_logic.model import *
from neo.ml_logic.registry import mlflow_run, mlflow_transition_model
from neo.ml_logic.registry import load_model, save_model, save_results
# from neo.ml_logic.preprocessor import preprocess_features     # Not yet exists...


def preprocess():

    data = pd.read_csv(DATA_LOCAL_PATH)

    data = clean_data(data)

    data = preprocessing(data)

    return data


def train(X_train, y_train):
    """
    Train the model, save it, and perform GridSearchCV.
    """
    # Load/init model
    pipeline = initialize_pipeline()

    # Define parameter grid
    param_grid = define_param_grid()

    # Perform grid search to find the best model
    grid_search = perform_grid_search(pipeline, param_grid, X_train, y_train)

    # Validation Score
    validation_score = np.float32(grid_search.best_score_)
    print(f"Validation Score: {validation_score:.4f}")

    return grid_search


def evaluate(grid_search, X_test, y_test):
    """
    Evaluate the model and return the evaluation score.
    """
    # Evaluate the model
    evaluation_score = np.float32(evaluate_best_model(grid_search, X_test, y_test))
    print(f"Evaluation Score: {evaluation_score:.4f}")

    return evaluation_score


def predict(grid_search, feature_input):
    """
    Load the model, predict based on feature input, and return the prediction.
    """
    # Predict using the model (alternatively load the saved model)
    # grid_search = joblib.load('best_model.pkl')  # If loading from a saved file

    # Predict the result
    prediction = grid_search.predict([feature_input])

    # Prediction as boolean
    prediction_bool = bool(prediction[0])
    print(f"Prediction: {prediction_bool}")

    return prediction_bool

# Example of loading features from an API (pseudo-code, replace with actual API function)
# feature_input = get_features_from_api()
# predict_with_model(grid_search, feature_input)



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
