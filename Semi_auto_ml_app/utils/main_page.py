import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import seaborn as sns

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


def main_page():
    """Main Page for Dataset Upload and Basic EDA"""
    st.subheader("Main Page")

    # Initialize a variable to hold the message
    message = ""

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