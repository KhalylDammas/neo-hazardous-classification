import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import resample

def peprocess(df):
    df_majority = df[df['is_hazardous'] == False]
    df_minority = df[df['is_hazardous'] == True]

    n_minority = len(df_minority)
    df_majority_downsampled = resample(df_majority,
                                   replace=False,
                                   n_samples=int(0.7 * (n_minority / 0.3)),  # 70% of the desired total size
                                   random_state=42)


    df_processed = pd.concat([df_majority_downsampled, df_minority])
    print(df_processed['is_hazardous'].value_counts(normalize=True) * 100)

    # drop columns
    df.drop(['neo_id','name','orbiting_body','estimated_diameter_min'], axis=1 , inplace = True )

    # Remove rows with any null values
    df.dropna(inplace=True)
    df.isnull().sum()

    X = df.drop(['is_hazardous'], axis=1)
    y = df['is_hazardous']

    # Initialize MinMaxScaler
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    df = pd.DataFrame(X_scaled, columns=X.columns) # @


    return df_processed
