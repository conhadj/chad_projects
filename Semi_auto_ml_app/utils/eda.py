import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run_eda():
    st.subheader("Exploratory Data Analysis")
    df = st.session_state['df']

    # Moved parts are now in main_page.py
    if st.checkbox("Correlation Plot(Matplotlib)"):
        numeric_df = df.select_dtypes(include='number')
        fig, ax = plt.subplots()
        ax.matshow(numeric_df.corr())
        plt.xticks(range(len(numeric_df.columns)), numeric_df.columns, rotation=90)
        plt.yticks(range(len(numeric_df.columns)), numeric_df.columns)
        st.pyplot(fig)

    if st.checkbox("Correlation Plot(Seaborn)"):
        numeric_df = df.select_dtypes(include='number')
        fig, ax = plt.subplots()
        sns.heatmap(numeric_df.corr(), annot=True, ax=ax)
        st.pyplot(fig)

    if st.checkbox("Pie Plot"):
        all_columns = df.columns.to_list()
        column_to_plot = st.selectbox("Select 1 Column", all_columns)

        if df[column_to_plot].dtype == 'object':
            if df[column_to_plot].nunique() <= 30:
                fig, ax = plt.subplots()
                pie_data = df[column_to_plot].value_counts()
                ax.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%", startangle=140)
                ax.axis('equal')
                st.pyplot(fig)
            else:
                st.warning("Selected column has more than 30 categories. Displaying a table instead.")
                value_counts = df[column_to_plot].value_counts().reset_index()
                value_counts.columns = [column_to_plot, 'Count']
                st.dataframe(value_counts)
        else:
            st.write("Selected column is not categorical or discrete numerical. Please select a categorical or discrete numerical column.")