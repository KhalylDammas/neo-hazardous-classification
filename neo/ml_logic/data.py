import numpy as np
import pandas as pd

from neo.params import *
# from sklearn.utils import resample
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler

# Added clean_data method...
def clean_data(df: pd.DataFrame) -> pd.DataFrame:

    # Drop unnecessary columns.
    df.drop(columns=['neo_id','name',
                     'orbiting_body',
                     'estimated_diameter_max'],inplace=True)

    # Drop missing values.
    df.dropna(inplace=True)

    # Remove outlier
    columns = ['absolute_magnitude', 'estimated_diameter_min', 'relative_velocity']
    outlier = []

    for column in columns:
       Q1 = df[column].quantile(0.25)
       Q3 = df[column].quantile(0.75)
       IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    column_outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)].index
    outlier.extend(column_outliers)

    outlier= list(set(outlier))
    df.drop(index=outlier , inplace=True)


    # Down sample the data.
    n_true = len(df.loc[df['is_hazardous'] == True])
    data_length = len(df.index)

    remove = data_length - int(MAJOR_RATIO * (n_true/(1-MAJOR_RATIO)) + n_true)
    df = df.drop(df.loc[df['is_hazardous'] == False].\
        sample(remove, random_state=RANDOM_STATE).index).reset_index(drop=True)

    return df

def preprocessing(df: pd.DataFrame) -> pd.DataFrame:

    assert isinstance(df, pd.DataFrame)

    #convert data type
    columns_to_convert = ['absolute_magnitude','estimated_diameter_min','relative_velocity','miss_distance','is_hazardous']
    df[columns_to_convert] = df[columns_to_convert].astype(np.float32)

    transformer = ColumnTransformer([
        ('MinMax_Scale', MinMaxScaler(), ['miss_distance']),
        ('Standard_Scale', StandardScaler(), ['absolute_magnitude', 'relative_velocity']),
        ('Robust_Scale', RobustScaler(), ['estimated_diameter_min'])
    ], remainder='passthrough')

    features_out = ['miss_distance', 'absolute_magnitude', 'relative_velocity',
                    'estimated_diameter_min', 'is_hazardous']

    df = transformer.fit_transform(df)

    df = pd.DataFrame(df, columns=features_out)

    assert isinstance(df, pd.DataFrame)

    return df
