from fastapi import FastAPI
from interface.main import predict
import pandas as pd
import pickle

# Initialize the FastAPI app
app = FastAPI()


# Prediction endpoint
@app.get("/prediction")
def prediction(
    absolute_magnitude: float,
    estimated_diameter_max: float,
    relative_velocity: float,
    miss_distance: float
):
    # Step 1: Prepare the input data as a DataFrame
    features = pd.DataFrame([{
        "absolute_magnitude": absolute_magnitude,
        "estimated_diameter_max": estimated_diameter_max,
        "relative_velocity": relative_velocity,
        "miss_distance": miss_distance,
    }])
    # Step 2: Use the pre-loaded model to make the prediction
    model = app.state.model
    prediction = predict(features)

    # Step 3: Return the prediction
    return {"prediction": prediction}


# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Nearest Earth Objects Prediction API!"}
