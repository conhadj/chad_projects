import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency, ttest_ind
from utils.streamlit_style import hide_streamlit_style

st.set_page_config(
    page_title="Materials And Mechanical Properties",
    page_icon="pictures/favicon.ico",
)

def perform_correlation_analysis(df):
    numeric_df = df.select_dtypes(include=np.number)
    correlation_matrix = numeric_df.corr()
    return correlation_matrix

def perform_t_test(df):
    numeric_df = df.select_dtypes(include=np.number)
    t_statistic, p_value = ttest_ind(numeric_df[numeric_df['Use'] == 0]['Su'], numeric_df[numeric_df['Use'] == 1]['Su'])
    return t_statistic, p_value

def perform_chi2_test(df):
    chi2_statistic, chi2_p_value, _, _ = chi2_contingency(pd.crosstab(df['Use'], df['rating']))
    return chi2_statistic, chi2_p_value

def plot_corr_matrix(df):
    fig, ax = plt.subplots()
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix Heatmap')
    st.pyplot(fig)

def calculate_z_scores_outliers(df):
    numeric_df = df.select_dtypes(include=np.number)
    z_scores = (numeric_df - numeric_df.mean()) / numeric_df.std()
    threshold = 3
    outliers = (z_scores.abs() > threshold)
    outlier_counts = outliers.sum()
    outlier_rows = df[outliers.any(axis=1)]
    return outlier_counts, outlier_rows

def handle_missing_values_and_outliers(df):
    numeric_df = df.select_dtypes(include=np.number)

    # Convert DataFrame to NumPy array
    numeric_array = numeric_df.to_numpy()

    # Replace masked values with NaN
    numeric_array = np.where(np.isinf(numeric_array), np.nan, numeric_array)

    # Check for NaN values
    nan_mask = np.isnan(numeric_array)

    # Count NaN values in each column
    nan_count = np.sum(nan_mask, axis=0)

    # Drop rows containing NaN values
    numeric_array = numeric_array[~np.any(nan_mask, axis=1)]

    # Calculate z-scores
    z_scores = (numeric_array - np.mean(numeric_array, axis=0)) / np.std(numeric_array, axis=0)

    # Define the threshold for identifying outliers
    threshold = 3
    outliers_after_processing = (z_scores > threshold) | (z_scores < -threshold)

    # Count of outliers in each column after processing
    outliers_after_processing_count = np.sum(outliers_after_processing, axis=0)

    return nan_count, outliers_after_processing_count

def corr_outliers():

    # Hide Streamlit style components
    hide_streamlit_style()

    if 'df_fe' not in st.session_state:
        st.warning("No data available. Please go to the 'Main Page' to load the data.")
        return

    df = st.session_state['df_fe']
    if 'rating' not in df.columns or 'Su/Sy' not in df.columns:
        st.warning("The dataframe does not contain the necessary columns ('rating' and 'Su/Sy'). Please make sure to apply the necessary feature engineering steps first.")
        return

    st.write("## 🧮 Correlation and Outliers Analysis")

    st.dataframe(df.head())

    if st.button('Perform Correlation Analysis'):
        st.write("### Correlation Analysis")
        st.write("""
            Correlation analysis measures the strength and direction of relationships between numerical variables.
            The correlation matrix provides a table showing the correlation coefficients between pairs of variables.
            Values range from -1 to 1, where 1 indicates a perfect positive correlation, -1 indicates a perfect negative correlation, and 0 indicates no correlation.
        """)
        correlation_matrix = perform_correlation_analysis(df)
        st.write("#### Correlation Matrix:")
        st.dataframe(correlation_matrix)

    if st.button('Plot Correlation Matrix'):
        plot_corr_matrix(df)

    if st.button('Perform T-Test'):
        st.write("### T-Test Analysis")
        st.write("""
            The T-Test is used to determine if there is a significant difference between the means of two groups.
            Here, it compares the 'Su' values (Ultimate Strength) across different 'Use' categories (0 and 1).
            A low p-value (< 0.05) indicates that the difference between group means is statistically significant.
        """)
        t_statistic, p_value = perform_t_test(df)
        st.success(f'T-Test Statistic: {t_statistic}')
        st.success(f'T-Test p-value: {p_value}')

    if st.button('Perform Chi-Square Test'):
        st.write("### Chi-Square Test Analysis")
        st.write("""
            The Chi-Square Test of Independence checks if there is a significant association between two categorical variables.
            Here, it tests the independence between 'Use' and 'Rating' categories.
            A low p-value (< 0.05) indicates that the variables are likely associated.
        """)
        chi2_statistic, chi2_p_value = perform_chi2_test(df)
        st.success(f'Chi-Square Statistic: {chi2_statistic}')
        st.success(f'Chi-Square p-value: {chi2_p_value}')

    st.write("---")

    if st.button('Calculate Z-Scores and Identify Outliers'):
        st.write("### Outlier Analysis and Handling")
        st.write("""
            Outliers are data points that differ significantly from other observations. They can be detected using z-scores, 
            which measure how many standard deviations a data point is from the mean. A common threshold for identifying outliers 
            is a z-score greater than 3 or less than -3.
        """)
        outlier_counts, outlier_rows = calculate_z_scores_outliers(df)
        st.write("#### Count of Outliers in Each Column:")
        st.text(outlier_counts)
        st.write("#### Rows Containing Outliers:")
        st.dataframe(outlier_rows)

    if st.button('Handle Missing Values'):
        st.write("### Handle Missing Values and Outliers")
        st.write("""
            This function handles missing values by removing rows containing NaN values and then recalculates the outliers.
            It provides the count of NaN values in each column and the count of outliers after processing.
        """)
        nan_count, outliers_after_processing_count = handle_missing_values_and_outliers(df)
        st.write("#### Count of NaN Values in Each Column:")
        st.text(pd.Series(nan_count, index=df.select_dtypes(include=np.number).columns))
        st.write("#### Count of Outliers in Each Column After Processing:")
        st.text(pd.Series(outliers_after_processing_count, index=df.select_dtypes(include=np.number).columns))

if __name__ == "__main__":
    corr_outliers()