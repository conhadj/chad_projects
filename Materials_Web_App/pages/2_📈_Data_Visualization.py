import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.streamlit_style import hide_streamlit_style

st.set_page_config(
    page_title="Materials And Mechanical Properties",
    page_icon="pictures/favicon.ico",
)

# @st.cache_data
def get_data():
    df = pd.read_csv("data/material.csv")
    return df

def plot_scatter_yield_vs_young(df):
    fig, ax = plt.subplots()
    ax.scatter(df['Sy'], df['E'], c='blue', alpha=0.5)
    ax.set_xlabel('Yield Strength (Sy)')
    ax.set_ylabel("Young's Modulus (E)")
    ax.set_title("Scatter plot of Yield Strength vs. Young's Modulus")
    ax.grid(True)
    st.pyplot(fig)

def plot_box_young_diff_usages(df):
    fig, ax = plt.subplots()
    sns.boxplot(x='Use', y='E', data=df, ax=ax)
    ax.set_xlabel('Usage')
    ax.set_ylabel("Young's Modulus (E)")
    ax.set_title("Box plot of Young's Modulus for Different Usages")
    ax.set_xticklabels(['False', 'True'])
    st.pyplot(fig)

def plot_pair_numericals(df):
    pair_plot = sns.pairplot(df.drop(columns=['Use', 'Ro']), diag_kind='kde')
    pair_plot.fig.suptitle('Pairplot of Numerical Variables', y=1.02)  # Adjust the title position
    st.pyplot(pair_plot.fig)

def plot_hist_material_density(df):
    fig, ax = plt.subplots()
    plt.hist(df['Ro'], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
    plt.xlabel('Density (Ro)')
    plt.ylabel('Frequency')
    plt.title('Histogram of Material Density')
    st.pyplot(fig)

def plot_scatter_ultimage_vs_yield_strength(df):
    fig, ax = plt.subplots()
    sns.scatterplot(x='Su', y='Sy', hue='Use', data=df)
    plt.xlabel('Ultimate Strength (Su)')
    plt.ylabel('Yield Strength (Sy)')
    plt.title('Scatter plot of Ultimate Strength vs. Yield Strength (Colored by Usage)')
    plt.legend(title='Usage')
    st.pyplot(fig)

def data_visualization():
    # Hide Streamlit style components
    hide_streamlit_style()

    if 'df' not in st.session_state:
        st.warning("No data available. Please go to the 'Main Page' to load the data.")
        return

    df = st.session_state['df']

    st.write("## 📈 Data Visualisation")

    st.dataframe(df.head())

    if 'df' not in st.session_state:
        st.session_state['df'] = df



    # Checkbox to show scatter plot
    if st.checkbox('Scatter plot of Yield Strength vs. Young\'s Modulus'):
        plot_scatter_yield_vs_young(df)

    if st.checkbox('Box plot of Young\'s Modulus for Different Usages'):
        plot_box_young_diff_usages(df)

    if st.checkbox('Pairplot of Numerical variables'):
        plot_pair_numericals(df)

    if st.checkbox('Histogram of Material Density'):
        plot_hist_material_density(df)

    if st.checkbox('Scatter plot of Ultimate Strength vs. Yield Strength (Colored by Usage)'):
        plot_scatter_ultimage_vs_yield_strength(df)


if __name__ == "__main__":
    data_visualization()