import pandas as pd

from neo.ml_logic.registry import *
from neo.params import *

from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

def initialize_model(load:bool=False) -> Pipeline:
    """
    Initialize the Model, or if `load` = True loads a saved model (if exists).
    """
    if load:
        model = model_load()
        if model != None:
            print("✅ Model Loaded")
            return model

    hyperparams = { #(C=100, gamma=1, kernel='rbf')
        'C':100,
        'kernel':'rbf',
        'gamma':1
    }
    svc = SVC(**hyperparams)
    model = Pipeline([
        ('classifier', svc)  # Placeholder classifier to be replaced in GridSearchCV
    ])

    print("✅ Model initialized")

    return model

def model_fit(model:Pipeline, X:pd.DataFrame, y:pd.DataFrame,
              X_val:pd.DataFrame=None, y_val:pd.DataFrame=None,
              val_ratio:float=0.2) -> dict:
    '''
    Train the model and evaluate its pervormance...

    '''
    ## EDIT Include -- Now Training -- flag...
    print("Start model Training...")
    if X_val != None and y_val != None:
        results = {
            'model':model.fit(X, y),
            'score':model.score(X_val, y_val)
        }

    else:
        X_train, X_test, y_train, y_test = \
            train_test_split(X, y, test_size=val_ratio,
                             random_state=RANDOM_STATE,
                             shuffle=True, stratify=y)

        results = {
            'model':model.fit(X_train, y_train),
            'score':model.score(X_test, y_test)
        }
    print("✅ Model Trained")
    return results


def define_param_grid():
    """
    Define the hyperparameter grid for different classifiers (Logistic Regression, SVM, KNN).
    """
    param_grid = [
        # Logistic Regression parameters
        {'classifier': [LogisticRegression()],
         'classifier__C': [0.01, 0.1, 1, 10, 100]},

        # SVM (Linear Kernel) parameters
        {'classifier': [SVC(kernel='linear')],
         'classifier__C': [0.01, 0.1, 1, 10, 100]},

        # SVM (RBF Kernel) parameters
        {'classifier': [SVC(kernel='rbf')],
         'classifier__C': [0.01, 0.1, 1, 10, 100],
         'classifier__gamma': ['scale', 0.001, 0.01, 0.1, 1]},

        # K-Nearest Neighbors parameters
        {'classifier': [KNeighborsClassifier()],
         'classifier__n_neighbors': [3, 5, 7, 9, 11]}
    ]

    print("✅ Parameter grid defined")
    return param_grid


def perform_grid_search(pipeline, param_grid, X_train, y_train):
    """
    Perform GridSearchCV to find the best hyperparameters from the parameter grid.
    """
    grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
    grid_search.fit(X_train, y_train)

    print("✅ Grid search complete")
    return grid_search


def evaluate_model(model, X_test, y_test):
    """
    Evaluate the Model on the test set and return the accuracy score.
    """
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print("✅ Model evaluated")
    print(f'Model accuracy on the test set: {accuracy:.4f}')
    return accuracy


# Example usage
if __name__ == '__main__':
    # Assume X_train, X_test, y_train, y_test are pre-defined
    # You can load your dataset here and split it into training and testing sets

    # 1. Initialize the pipeline
    pipeline = initialize_model()

    # 2. Define the parameter grid
    param_grid = define_param_grid()

    # 3. Perform grid search to find the best model
    grid_search = perform_grid_search(pipeline, param_grid, X_train, y_train)

    # 4. Evaluate the best model
    evaluate_best_model(grid_search, X_test, y_test)

    # 5. Print the best parameters found by GridSearchCV
    print("Best parameters found by GridSearchCV:")
    print(grid_search.best_params_)
