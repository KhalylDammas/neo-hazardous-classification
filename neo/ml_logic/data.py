import numpy as np
import pandas as pd

from neo.params import *
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler

# load data
df = pd.read_csv(DATA_LOCAL_PATH)

# Added clean_data method...
def clean_data(df: pd.DataFrame) -> pd.DataFrame:

    # Drop unnecessary columns.
    df.drop(columns=['neo_id','name',
                     'orbiting_body',
                     'estimated_diameter_max'],inplace=True)

    # Drop missing values.
    df.dropna(inplace=True)

    # Store the original number of rows for comparison
    original_row_count = df.shape[0]

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

    # Assertions to verify the output
    assert 'neo_id' not in df.columns, "Error: Column 'neo_id' should have been dropped."
    print("Success: Column 'neo_id' has been dropped.")

    assert not df.isna().any().any(), "Error: There should be no missing values."
    print("Success: No missing values.")

    assert isinstance(df, pd.DataFrame), "Error: The output should be a pandas DataFrame."
    print("Success: Output is a pandas DataFrame.")

    # Assertion to check if the number of rows has decreased
    new_row_count_after_outliers = df.shape[0]
    print(f"Original row count: {original_row_count}, New row count after removing outliers: {new_row_count_after_outliers}")
    assert new_row_count_after_outliers < original_row_count, "Error: The number of rows did not decrease after removing outliers."

    # Assertion to check the number of rows after downsampling
    new_row_count_after_downsampling = df.shape[0]
    print(f"New row count after downsampling: {new_row_count_after_downsampling}, Original data length: {data_length}")
    assert new_row_count_after_downsampling <= data_length, "Error: The number of rows after downsampling exceeds the original number."

    return df


class pre_processor():

    def __init__(self):
        self.transformer = ColumnTransformer([
            ('MinMax_Scale', MinMaxScaler(), ['miss_distance']),
            ('Standard_Scale', StandardScaler(), ['absolute_magnitude', 'relative_velocity']),
            ('Robust_Scale', RobustScaler(), ['estimated_diameter_min'])
        ], remainder='drop')

        self.features_out = ['miss_distance', 'absolute_magnitude',
                             'relative_velocity','estimated_diameter_min']

    def fit(self, df:pd.DataFrame) -> None:
        self.transformer.fit(df)

    def transform(self, df:pd.DataFrame) -> pd.DataFrame:

        df = self.transformer.transform(df)

        df = pd.DataFrame(df, columns=self.features_out)

        assert df.shape[1] == len(self.features_out), "Error: The number of output columns is incorrect."
        print("Success: The number of output columns is correct.")

        assert isinstance(df, pd.DataFrame), "Error: The output should be a pandas DataFrame."
        print("Success: Output is a pandas DataFrame.")

        return df
