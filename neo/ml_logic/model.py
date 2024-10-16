import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score


def initialize_pipeline():
    """
    Initialize the Pipeline with MinMaxScaler and a default classifier (LogisticRegression).
    """
    pipeline = Pipeline([
        ('scaler', MinMaxScaler()),  # Scale features to [0, 1]
        ('classifier', LogisticRegression())  # Placeholder classifier to be replaced in GridSearchCV
    ])

    print("✅ Pipeline initialized")
    return pipeline


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


def evaluate_best_model(grid_search, X_test, y_test):
    """
    Evaluate the best model from GridSearchCV on the test set and return the accuracy score.
    """
    y_pred = grid_search.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print("✅ Best model evaluated")
    print(f'Best model accuracy on the test set: {accuracy:.4f}')
    return accuracy


# Example usage
if __name__ == '__main__':
    # Assume X_train, X_test, y_train, y_test are pre-defined
    # You can load your dataset here and split it into training and testing sets

    # 1. Initialize the pipeline
    pipeline = initialize_pipeline()

    # 2. Define the parameter grid
    param_grid = define_param_grid()

    # 3. Perform grid search to find the best model
    grid_search = perform_grid_search(pipeline, param_grid, X_train, y_train)

    # 4. Evaluate the best model
    evaluate_best_model(grid_search, X_test, y_test)

    # 5. Print the best parameters found by GridSearchCV
    print("Best parameters found by GridSearchCV:")
    print(grid_search.best_params_)
