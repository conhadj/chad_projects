import streamlit as st
from utils.streamlit_style import hide_streamlit_style

st.set_page_config(
    page_title="Materials And Mechanical Properties",
    page_icon="pictures/favicon.ico",
    layout="wide"
)

def about():

    # Hide Streamlit style components
    hide_streamlit_style()

    st.write("## 📑 About")
    st.write("Constantinos Hadjigregoriou")
    st.write("constantinos.hadjigregoriou@outlook.com")

if __name__ == "__main__":
    about()