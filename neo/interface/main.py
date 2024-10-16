import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

from neo.params import *
from neo.ml_logic.data import  clean_data, load_data
from neo.ml_logic.model import initialize_model, compile_model, train_model, evaluate_model
from neo.ml_logic.preprocessor import preprocess_features
from neo.ml_logic.registry import load_model, save_model, save_results
from neo.ml_logic.registry import mlflow_run, mlflow_transition_model


def preprocess():
    data = load_data()

    cleaned_data = clean_data(data)
    return cleaned_data





def train_model(X_train, y_train):
    model = LinearRegression()  # Simple linear regression model
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)  # Calculate mean absolute error
    return mae

def predict(model, X_new):
    return model.predict(X_new)

if __name__ == '__main__':
    # Load the data
    data = load_data()
    data = clean_data(data)

    # Prepare the data
    X = data[['absolute_magnitude','estimated_diameter_min','relative_velocity','miss_distance']]
    y = data['is_hazardous']

    # Split the data into training and validation sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = train_model(X_train, y_train)

    # Evaluate the model
    mae = evaluate_model(model, X_test, y_test)
    print(f'MAE: {mae}')

    # Predict on new data
    X_new = pd.DataFrame({
        'absolute_magnitude': [-73.950655],
        'estimated_diameter_min': [40.783282],
        'relative_velocity': [-73.984365],
        'miss_distance': [40.769802]
    })
    y_pred = predict(model, X_new)
    print(f'Predicted Fare: {y_pred[0]}')
