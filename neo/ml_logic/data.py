import pandas as pd
from neo.params import *

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # drop columns
    df.drop(['neo_id','name','orbiting_body','estimated_diameter_min'], axis=1 , inplace = True )
    # Remove rows with any null values
    df.dropna()
    return df

def load_data():
    df = pd.read_csv("~/code/KhalylDammas/neo-hazardous-classification/raw data/nearest-earth-objects(1910-2024).csv")
    return df
