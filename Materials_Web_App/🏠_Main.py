import streamlit as st
import pandas as pd
from utils.streamlit_style import hide_streamlit_style

def get_data():
    df = pd.read_csv("data/material.csv")
    return df

st.set_page_config(
    page_title="Materials And Mechanical Properties",
    page_icon="pictures/favicon.ico",
    layout="wide"
)

# Hide Streamlit style components
hide_streamlit_style()


st.write("# Welcome to the Materials And Mechanical Properties App! 👋")

st.sidebar.success("Select a page above.")

st.markdown("<br><br>", unsafe_allow_html=True) 
st.markdown(
    """
    This app helps you visualize and analyze Materials and their Mechanical properties.
    **👈 Select a page from the sidebar** to see some examples
    of what this app can do!
    """
)

# Display local image
image_path = "pictures/main_page_background.jpeg"
st.image(image_path, use_column_width=True)

df = get_data()

if 'df' not in st.session_state:
    st.session_state['df'] = df