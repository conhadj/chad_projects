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
    st.write("👤 Constantinos Hadjigregoriou")
    st.write("📧 [Email](mailto:constantinos.hadjigregoriou@outlook.com)")
    st.write("🐙 [Project's GitHub Repository](https://github.com/conhadj/chad_projects/tree/main/Materials_and_their_Mechanical_Properties)")

if __name__ == "__main__":
    about()