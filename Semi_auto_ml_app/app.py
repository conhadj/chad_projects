import streamlit as st
from utils.main_page import main_page
from utils.eda import run_eda
from utils.plots import run_plots
from utils.model_building import run_model_building
from utils.data_preprocessing import run_preprocess
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="AutoML Alchemist",  
    page_icon="favicon.ico",  
    layout="centered",  
    initial_sidebar_state="expanded"  
)

# Function to handle the main page and dataset upload
def main():
    """Semi Automated ML App with Streamlit"""
    
    activities = ["Main", "EDA", "Plots", "Data Preprocessing", "Model Building", "About"]
    choice = st.sidebar.selectbox("Select Activities", activities)

    if choice == 'Main':
        main_page()
    
    elif choice == 'EDA':
        if 'df' in st.session_state:
            run_eda()
        else:
            st.write("Please upload a dataset from the Main page.")
    
    elif choice == 'Plots':
        if 'df' in st.session_state:
            run_plots()
        else:
            st.write("Please upload a dataset from the Main page.")

    elif choice == 'Data Preprocessing':
        if 'df' in st.session_state:
            run_preprocess()
        else:
            st.write("Please upload a dataset from the Main page.")
    
    elif choice == 'Model Building':
        if 'df' in st.session_state:
            run_model_building()
        else:
            st.write("Please upload a dataset from the Main page.")
    
    elif choice == 'About':
        st.subheader("About")
        st.write("Constantinos Hadjigregoriou")
        st.write("constantinos.hadjigregoriou@outlook.com")

if __name__ == '__main__':
	main()