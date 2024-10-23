import pandas as pd

from neo.params import *
from neo.ml_logic.data import  *
from neo.ml_logic.model import *

from sklearn.model_selection import train_test_split

def preprocess(transformer:object, fit=False) -> tuple:
    '''
    Pre-Precesses the data.
    Remove outliers and missing values, Balances the classes ratio.
    ~~
    Parameters:
    - `data`:pd.DataFrane ->
    - `transformer`:object -> The pre-processor object.
    - `fit`:bool -> A flag to specify the pre-processing mode for either fit and transform then return the processed data, or to return the fitted transformer only.
    __
    Return:
    If fit = True.
    - `transformer`:pre-processor -> Fitted transformer.
    if fit = False.
    - `data_dict`:dict, `transformer`:pre-processor -> A dictionary contatins all data splits train/val/test X/y, fitted transformer.
    '''
    data = pd.read_csv(DATA_LOCAL_PATH)

    data = clean_data(data)

    X = data.drop(columns=['is_hazardous'])
    y = data['is_hazardous']

    X_train, X_test, y_train, y_test = \
    train_test_split(X, y, test_size=0.2,
                        random_state=RANDOM_STATE,
                        shuffle=True, stratify=y)

    X_train, X_val, y_train, y_val = \
    train_test_split(X_train, y_train, test_size=0.25,
                        random_state=RANDOM_STATE,
                        shuffle=True, stratify=y_train)

    transformer.fit(X_train)
    if fit:
        return transformer

    X_train = transformer.transform(X_train)
    X_test = transformer.transform(X_test)
    X_val = transformer.transform(X_val)

    data_dict = {
        'train': (X_train, y_train),
        'val': (X_val, y_val),
        'test': (X_test, y_test)
    }

    return data_dict, transformer


def train(X_train, y_train, X_val, y_val, load=False):
    """
    Train the model, save it, and perform GridSearchCV.
    """

    # Load/init model
    if load:
        model = initialize_model(load=load)
        results = {
            'model':model,
            'score':model.score(X_val, y_val)
        }
    else:
        # Model fit..
        results = model_fit(model=model, X=X_train, y=y_train, X_val=X_val, y_val=y_val)

    # Validation Score
    validation_score = results['score']
    print(f"Validation Score: {validation_score:.4f}")

    return results['model']


def evaluate(model, X_test, y_test):
    """
    Evaluate the model and return the evaluation score.
    """

    print("Model Evaluation...")
    evaluation_score = evaluate_model(model=model, X_test=X_test, y_test=y_test)

    print(f"Evaluation Score: {evaluation_score:.4f}")

    return evaluation_score


def predict(X, model=None):
    """
    Load the model, predict based on feature input, and return the prediction.
    """
    transformer = pre_processor()
    transformer = preprocess(transformer, fit=True)
    if model is None:
        model = initialize_model(load=True)
    # Predict the result
    X = transformer.transform(X)
    prediction = model.predict(X)

    # Prediction as boolean
    prediction_bool = bool(prediction[0])
    print(f"Prediction: {prediction_bool}")

    return prediction_bool


if __name__ == '__main__':
    breakpoint()

    transformer = pre_processor()

    data_dict, transformer = preprocess(transformer)

    X_train, y_train = data_dict['train']
    X_val, y_val = data_dict['val']
    X_test, y_test = data_dict['test']


    model = train(X_train, y_train, X_val, y_val, load=True)

    score = evaluate(model, X_test, y_test)

    # Predict on new data
    X_new = pd.DataFrame({
        'miss_distance': [10548.158],
        'absolute_magnitude': [-73.950655],
        'relative_velocity': [-73.984365],
        'estimated_diameter_min': [40.783282],
    })

    y_pred = predict(X_new, model)
