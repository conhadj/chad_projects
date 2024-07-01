import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def run_plots():
    st.subheader("Data Visualization")
    data = st.file_uploader("Upload a Dataset", type=["csv", "txt"])
    if data is not None:
        df = pd.read_csv(data)
        st.dataframe(df.head())

        if st.checkbox("Show Value Counts"):
            fig, ax = plt.subplots()
            df.iloc[:, -1].value_counts().plot(kind='bar', ax=ax)
            st.pyplot(fig)

        all_columns_names = df.columns.tolist()
        type_of_plot = st.selectbox("Select Type of Plot", ["area", "bar", "line", "hist", "box", "kde"])
        selected_columns_names = st.multiselect("Select Columns To Plot", all_columns_names)

        if st.button("Generate Plot"):
            if type_of_plot in ["area", "bar", "line"]:
                cust_data = df[selected_columns_names]
                st.success(f"Generating Customizable Plot of {type_of_plot} for {selected_columns_names}")
                if type_of_plot == 'area':
                    st.area_chart(cust_data)
                elif type_of_plot == 'bar':
                    st.bar_chart(cust_data)
                elif type_of_plot == 'line':
                    st.line_chart(cust_data)
            else:
                numeric_columns = df[selected_columns_names].select_dtypes(include='number').columns.tolist()
                if not numeric_columns:
                    st.error("No numeric columns selected. Please select at least one numeric column for the chosen plot type.")
                else:
                    st.success(f"Generating Customizable Plot of {type_of_plot} for {numeric_columns}")
                    fig, ax = plt.subplots()
                    df[numeric_columns].plot(kind=type_of_plot, ax=ax)
                    st.pyplot(fig)