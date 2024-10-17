import numpy as np
import pandas as pd

from neo.params import *
# from sklearn.utils import resample
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler

# Added `clean_data` method...
def clean_data(df: pd.DataFrame) -> pd.DataFrame:

    # Drop unnecessary columns.
    df.drop(columns=['neo_id','name',
                     'orbiting_body',
                     'estimated_diameter_max'],inplace=True)

    # Drop missing values.
    df.dropna(inplace=True)

    # Down sample the data.
    n_true = len(df.loc[df['is_hazardous'] == True])
    data_length = len(df.index)

    remove = data_length - int(MAJOR_RATIO * (n_true/(1-MAJOR_RATIO)) + n_true)
    df = df.drop(df.loc[df['is_hazardous'] == False].\
        sample(remove, random_state=RANDOM_STATE).index).reset_index(drop=True)

    return df

# Changed method name. (peprocess -> preprocessing)
def preprocessing(df: pd.DataFrame) -> pd.DataFrame:

    assert isinstance(df, pd.DataFrame)

    transformer = ColumnTransformer([
        ('MinMax_Scale', MinMaxScaler(), ['miss_distance']),
        ('Standard_Scale', StandardScaler(), ['absolute_magnitude', 'relative_velocity']),
        ('Robust_Scale', RobustScaler(), ['estimated_diameter_min'])
    ], remainder='passthrough')

    # Initialize MinMaxScaler
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    df = pd.DataFrame(X_scaled, columns=X.columns) # @
    
    df = transformer.fit_transform(df)
    
    #convert data type
    columns_to_convert = ['absolute_magnitude','estimated_diameter_min','relative_velocity','miss_distance','is_hazardous']

    df[columns_to_convert] = df[columns_to_convert].astype(np.float32)

    return df