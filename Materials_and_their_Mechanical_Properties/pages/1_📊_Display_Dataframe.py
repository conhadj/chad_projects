import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import numpy as np
from utils.streamlit_style import hide_streamlit_style

st.set_page_config(
    page_title="Materials And Mechanical Properties",
    page_icon="pictures/favicon.ico",
    layout="wide"
)

# Function to add material groups
def add_material_groups(df):
    conditions = [
        df["Material"].str.contains("ANSI Steel"),
        df["Material"].str.contains("ANSI Aluminum Alloy"),
        df["Material"].str.contains("GOST Steel"),
        df["Material"].str.contains("ISO EN"),
        df["Material"].str.contains("DIN"),
        df["Material"].str.contains("BS"),
        df["Material"].str.contains("NF"),
        df["Material"].str.contains("CSN")
    ]
    choices = [
        "ANSI Steel",
        "ANSI Aluminum Alloy",
        "GOST Steel",
        "ISO EN",
        "DIN",
        "BS",
        "NF",
        "CSN"
    ]
    df["Material Group"] = np.select(conditions, choices, default="Other")
    return df

# Function to display top KPIs
def display_kpis(df_selection):
    average_yield_strength = round(df_selection["Sy"].mean(), 2)
    average_ultimate_strength = round(df_selection["Su"].mean(), 2)
    average_modulus = round(df_selection["E"].mean(), 2)

    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.subheader("Average Yield Strength:")
        st.subheader(f"{average_yield_strength} MPa")
    with middle_column:
        st.subheader("Average Ultimate Strength:")
        st.subheader(f"{average_ultimate_strength} MPa")
    with right_column:
        st.subheader("Average Young's Modulus:")
        st.subheader(f"{average_modulus} GPa")

# Function to plot Yield Strength by Material Group
def plot_yield_strength(df_selection):
    yield_strength_by_material = df_selection.groupby(by=["Material Group"])[["Sy"]].mean().sort_values(by="Sy")
    fig_yield_strength = px.bar(
        yield_strength_by_material,
        x="Sy",
        y=yield_strength_by_material.index,
        orientation="h",
        title="<b>Yield Strength by Material Group</b>",
        color_discrete_sequence=["#2E3092"] * len(yield_strength_by_material),
        template="plotly_white",
    )
    fig_yield_strength.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )
    return fig_yield_strength

# Function to plot Ultimate Strength by Material Group
def plot_ultimate_strength(df_selection):
    ultimate_strength_by_material = df_selection.groupby(by=["Material Group"])[["Su"]].mean().sort_values(by="Su")
    fig_ultimate_strength = px.bar(
        ultimate_strength_by_material,
        x="Su",
        y=ultimate_strength_by_material.index,
        orientation="h",
        title="<b>Ultimate Strength by Material Group</b>",
        color_discrete_sequence=["#2E3092"] * len(ultimate_strength_by_material),
        template="plotly_white",
    )
    fig_ultimate_strength.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )
    return fig_ultimate_strength

# Function to plot Young's Modulus by Material Group
def plot_modulus(df_selection):
    modulus_by_material = df_selection.groupby(by=["Material Group"])[["E"]].mean().sort_values(by="E")
    fig_modulus = px.bar(
        modulus_by_material,
        x="E",
        y=modulus_by_material.index,
        orientation="h",
        title="<b>Young's Modulus by Material Group</b>",
        color_discrete_sequence=["#2E3092"] * len(modulus_by_material),
        template="plotly_white",
    )
    fig_modulus.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )
    return fig_modulus

def display_dataframe():
    # Hide Streamlit style components
    hide_streamlit_style()

    if 'df' not in st.session_state:
        st.warning("No data available. Please go to the 'Main Page' to load the data.")
        return

    #df = st.session_state['df']

    df = add_material_groups(st.session_state['df'].copy())  # Add material groups

    # ---- SIDEBAR ----
    st.sidebar.header("Please Filter Here:")
    material_group_filter = st.sidebar.multiselect(
        "Select the Material Group:",
        options=df["Material Group"].unique(),
        default=df["Material Group"].unique()
    )

    # Apply the material group filter
    df_selection = df[df["Material Group"].isin(material_group_filter)]

    # Check if the dataframe is empty:
    if df_selection.empty:
        st.warning("No data available based on the current filter settings!")
        st.stop()  # This will halt the app from further execution.

    # ---- MAINPAGE ----
    st.markdown("## 📊 Materials Dashboard")

    display_kpis(df_selection)  # Display KPIs

    st.markdown("""---""")

    # Plot Yield Strength by Material Group
    fig_yield_strength = plot_yield_strength(df_selection)
    st.plotly_chart(fig_yield_strength, use_container_width=True)

    # Plot Ultimate Strength by Material Group
    fig_ultimate_strength = plot_ultimate_strength(df_selection)
    st.plotly_chart(fig_ultimate_strength, use_container_width=True)

    # Plot Young's Modulus by Material Group
    fig_modulus = plot_modulus(df_selection)
    st.plotly_chart(fig_modulus, use_container_width=True)


if __name__ == "__main__":
    hide_streamlit_style()
    display_dataframe()