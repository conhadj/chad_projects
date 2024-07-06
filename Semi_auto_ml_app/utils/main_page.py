import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import seaborn as sns
from utils.data_utils import categorize_columns


def styled_message(message):
    """Function to return a styled message"""
    return f"""
    <div style="background-color: #d4edda; padding: 10px; border-radius: 5px;">
        {message}
    </div>
    """

def plot_null_heatmap(df):
    """Function to plot null value heatmap using Seaborn"""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(df.isnull(), cbar=False, cmap='viridis', yticklabels=False, ax=ax)
    st.pyplot(fig)

def show_value_counts(df):
    """Function to display value counts for selected column"""
    column_to_display = st.selectbox("Select Column", df.columns)
    

    if column_to_display is not None:
        value_counts_series = df[column_to_display].value_counts()
        st.write(value_counts_series)

def plot_mean_values(df, column):
    """Function to plot mean values heatmap for selected column"""
    unique_values = df[column].unique()
    colors = ['#5DADE2', '#E0E0E0']
    
    num_unique_values = len(unique_values)
    num_cols = 2  # Adjust this value based on your preferred layout
    num_rows = (num_unique_values + num_cols - 1) // num_cols  # Calculate the number of rows needed

    fig, ax = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(10, 5 * num_rows))

    # Ensure ax is always a 2D array for easier indexing
    if num_rows == 1 and num_cols == 1:
        ax = [[ax]]
    elif num_rows == 1:
        ax = [ax]
    elif num_cols == 1:
        ax = [[a] for a in ax]

    for i, value in enumerate(unique_values):
        row = i // num_cols
        col = i % num_cols
        data = df[df[column] == value].describe().T
        sns.heatmap(data[['mean']], annot=True, cmap=colors, linewidths=0.4, linecolor='black', cbar=False, fmt='.2f', ax=ax[row][col])
        ax[row][col].set_title(f'Mean Values: {value} {column}')
    
    # Remove any empty subplots
    for j in range(i + 1, num_rows * num_cols):
        row = j // num_cols
        col = j % num_cols
        fig.delaxes(ax[row][col])

    fig.tight_layout(pad=2)
    st.pyplot(fig)

def main_page():
    """Main Page for Dataset Upload and Basic EDA"""
    st.subheader("Main Page")

    # Initialize a variable to hold the message
    message = ""

    # Initialize the empty container
    placeholder = st.empty()
    
    # Reset button in the sidebar
    if st.sidebar.button('Reset Dataset'):

        if 'df' in st.session_state:
            # List of keys to delete from session state
            keys_to_delete = [
                'df', 
                'label_enc_complete', 
                'df_encoded', 
                'label_mappings', 
                'numerical_discrete_cols', 
                'numerical_continuous_cols', 
                'categorical_cols'
            ]

            # Delete each key if it exists in session state
            for key in keys_to_delete:
                if key in st.session_state:
                    del st.session_state[key]

            st.sidebar.success("Dataset reset successfully!")
            st.experimental_rerun()  # Rerun the app to reflect changes
            return  # Return immediately to refresh the UI
        else:
            st.sidebar.warning("No dataset to reset.")

        # Return immediately to refresh the UI
        return

    with placeholder.container():
        if 'df' not in st.session_state:
            uploaded_data = st.file_uploader("Upload a Dataset", type=["csv", "txt"])
            if uploaded_data is not None:
                df = pd.read_csv(uploaded_data)
                st.dataframe(df.head())
                st.session_state['df'] = df
            else:
                st.write("Please upload a dataset to proceed.")
        else:
            df = st.session_state['df']
            st.dataframe(df.head())
        
        if 'df' in st.session_state:
            df = st.session_state['df']

            # Initialize variables to store label encoder results
            label_enc_complete = st.session_state.get('label_enc_complete', False)
            df_encoded = st.session_state.get('df_encoded', None)
            label_mappings = st.session_state.get('label_mappings', None)

             # Categorize columns into lists based on feature types
            numerical_discrete_cols, numerical_continuous_cols, categorical_cols = categorize_columns(df)
            st.session_state['numerical_discrete_cols'] = numerical_discrete_cols
            st.session_state['numerical_continuous_cols'] = numerical_continuous_cols
            st.session_state['categorical_cols'] = categorical_cols


            if st.checkbox("Show Shape"):
                st.write(df.shape)

            if st.checkbox("Show Columns"):
                all_columns = df.columns.to_list()
                st.write(all_columns)

            if st.checkbox("Information"):
                st.markdown(styled_message("Looking into numerical and categorical variables"), unsafe_allow_html=True)
                buffer = io.StringIO()
                df.info(buf=buffer)
                s = buffer.getvalue()
                st.text(s)
                
            if st.checkbox("Description"):
                st.markdown(styled_message("Looking into numerical features' statistics"), unsafe_allow_html=True)
                st.write(df.describe())


            if st.checkbox("Show Selected Columns"):
                selected_columns = st.multiselect("Select Columns", df.columns.to_list())
                new_df = df[selected_columns]
                st.dataframe(new_df)

            if st.checkbox("Show Value Counts"):
                show_value_counts(df)

            if st.checkbox("Show Null Counts in a Plot"):
                st.markdown(styled_message("Seaborn null values heatmap"), unsafe_allow_html=True)
                if df.isnull().any().any():
                    st.markdown(styled_message("Dataframe has null values"), unsafe_allow_html=True)
                else:
                    st.markdown(styled_message("Dataframe has no null values"), unsafe_allow_html=True)
                plot_null_heatmap(df)

            if st.checkbox("Show Mean Values"):
                columns_with_few_unique_values = [col for col in df.columns if df[col].nunique() <= 10]
                if columns_with_few_unique_values:
                    column_to_display = st.selectbox("Select Column", columns_with_few_unique_values)
                    plot_mean_values(df, column_to_display)
                else:
                    st.write("No columns with 10 or fewer unique values found.")


    # Display the message in a light green box
    if message:
        st.markdown(
            f"""
            <div style="background-color: #d4edda; padding: 10px; border-radius: 5px;">
                {message}
            </div>
            """, 
            unsafe_allow_html=True
        )