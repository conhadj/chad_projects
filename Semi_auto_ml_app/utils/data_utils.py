import pandas as pd 

# Sampling the dataset if it's too large
def sample_dataframe(df, max_samples=100000):
	if len(df) > max_samples:
		return df.sample(n=max_samples, random_state=42)
	else:
		return df

def check_variable_type(series):

	if series.dtype == 'object':
		return 'Categorical'

	unique_values = series.nunique()

	if unique_values < 5:
		return 'Numerical Binary' if unique_values == 2 else 'Numerical Multiclass'
	elif unique_values <= 20:
		return 'Mixed'
	else:
		return 'Numerical Continuous'

# Function to determine feature types
def determine_feature_type(df, col):
    # Determine data type
    if df[col].dtype == 'object':
        return "Categorical"
    elif pd.api.types.is_numeric_dtype(df[col]):
        if df[col].nunique() > 10:
            return "Numerical Continuous"
        else:
            if df[col].nunique() == 1:
                return "Numerical Discrete Single Variate"
            elif df[col].nunique() == 2:
                return "Numerical Discrete Binary"
            else:
                return "Numerical Discrete"
    elif pd.api.types.is_datetime64_any_dtype(df[col]):
        return "Date"
    else:
        return "Other"

# Function to categorize columns into different lists based on feature types
def categorize_columns(df):
    numerical_discrete_cols = []
    numerical_continuous_cols = []
    categorical_cols = []

    for col in df.columns:
        feature_type = determine_feature_type(df, col)
        if feature_type == "Numerical Discrete" or feature_type == "Numerical Discrete Single Variate" or feature_type == "Numerical Discrete Binary":
            numerical_discrete_cols.append(col)
        elif feature_type == "Numerical Continuous":
            numerical_continuous_cols.append(col)
        elif feature_type == "Categorical":
            categorical_cols.append(col)

    return numerical_discrete_cols, numerical_continuous_cols, categorical_cols