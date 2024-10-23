from fastapi import FastAPI
from neo.interface.main import predict
import pandas as pd

# Initialize the FastAPI app
app = FastAPI()


# Prediction endpoint
@app.get("/prediction")
def prediction(
    absolute_magnitude: float,
    estimated_diameter_min: float,
    relative_velocity: float,
    miss_distance: float
):
    # Step 1: Prepare the input data as a DataFrame
    features = pd.DataFrame([{
        "absolute_magnitude": absolute_magnitude,
        "estimated_diameter_min": estimated_diameter_min,
        "relative_velocity": relative_velocity,
        "miss_distance": miss_distance,
    }])
    # Step 2: Use the pre-loaded model to make the prediction
    # model = app.state.model
    prediction = predict(features)

    # Step 3: Return the prediction
    return {"prediction": prediction}
# http://127.0.0.1:8000/prediction?absolute_magnitude=0.0&estimated_diameter_min=0.0&relative_velocity=0.0&miss_distance=0.0

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Nearest Earth Objects Prediction API!"}
