import numpy as np
import pandas as pd

from neo.params import *
from neo.ml_logic.data import  *
from neo.ml_logic.model import *

from sklearn.model_selection import train_test_split

def preprocess(test=True):

    data = pd.read_csv(DATA_LOCAL_PATH)

    data = clean_data(data)

    data = preprocessing(data)
    if test:
        return data
    X = data.drop(columns=['is_hazardous'])
    y = data['is_hazardous']

    return X, y


def train(X_train, y_train):
    """
    Train the model, save it, and perform GridSearchCV.
    """
    # Load/init model
    model = initialize_model()

    # Define parameter grid
    # param_grid = define_param_grid()

    # Model fit..
    results = model_fit(model=model, X=X_train, y=y_train)

    # Perform grid search to find the best model
    # grid_search = perform_grid_search(pipeline, param_grid, X_train, y_train)

    # Validation Score
    # validation_score = np.float32(grid_search.best_score_)
    validation_score = results['score']
    print(f"Validation Score: {validation_score:.4f}")

    return results['model']


def evaluate(model, X_test, y_test):
    """
    Evaluate the model and return the evaluation score.
    """
    # Evaluate the model
    # evaluation_score = np.float32(evaluate_best_model(grid_search, X_test, y_test))

    evaluation_score = evaluate_model(model=model, X_test=X_test, y_test=y_test)

    print(f"Evaluation Score: {evaluation_score:.4f}")

    return evaluation_score


def predict(model, feature_input):
    """
    Load the model, predict based on feature input, and return the prediction.
    """
    # Predict using the model (alternatively load the saved model)
    # grid_search = joblib.load('best_model.pkl')  # If loading from a saved file

    # Predict the result
    prediction = model.predict([feature_input])

    # Prediction as boolean
    prediction_bool = bool(prediction[0])
    print(f"Prediction: {prediction_bool}")

    return prediction_bool

# Example of loading features from an API (pseudo-code, replace with actual API function)
# feature_input = get_features_from_api()
# predict_with_model(grid_search, feature_input)



if __name__ == '__main__':

    X, y = preprocess(False)

    X_train, X_test, y_train, y_test = \
    train_test_split(X, y, test_size=0.2,
                        random_state=RANDOM_STATE,
                        shuffle=True, stratify=y)

    model = train(X_train, y_train)

    score = evaluate(model, X_test, y_test)

    # Predict on new data
    X_new = pd.DataFrame({
        'miss_distance': [10548.158],
        'absolute_magnitude': [-73.950655],
        'relative_velocity': [-73.984365],
        'estimated_diameter_min': [40.783282],
        'miss_distance': [40.769802]
    })

    # y_pred = predict(model, X_new)
    # print(f'Predicted Fare: {y_pred[0]}')
