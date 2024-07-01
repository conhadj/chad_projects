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