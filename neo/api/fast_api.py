from fastapi import FastAPI
import pandas as pd
import pickle

# Initialize the FastAPI app
app = FastAPI()

# Prediction endpoint
@app.get("/predict")
def predict(
    absolute_magnitude: float,
    estimated_diameter_max: float,
    relative_velocity: float,
    miss_distance: float
):
    """
    Make a prediction for the Nearest Earth Objects based on provided features.
    """
    # Step 1: Prepare the input data as a DataFrame
    features = pd.DataFrame([{
        "absolute_magnitude": absolute_magnitude,
        "estimated_diameter_max": estimated_diameter_max,
        "relative_velocity": relative_velocity,
        "miss_distance": miss_distance,
    }])

    # Step 2: Preprocess the features using the pre-loaded pipeline
    preprocessed_features = app.state.model.named_steps['preprocessing'].transform(features)

    # Step 3: Use the pre-loaded pipeline to make the prediction
    prediction = app.state.model.named_steps['classifier'].predict(preprocessed_features)

    # Step 4: Return the prediction in a JSON format
    return {"prediction": prediction[0]}

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Nearest Earth Objects Prediction API!"}

#preprocessing feature, using function that is already created. You will only do preprocessing.transform(features) ✅
#Export the trained model as a pickle file in the notebook
#Import the model pickle file in the app.py ✅
#Do model.predict with the preprocessed features
#Return the prediction ✅
