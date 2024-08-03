import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils.plot_settings import apply_plot_settings, apply_axes_settings
from utils.streamlit_style import hide_streamlit_style

st.set_page_config(
    page_title="Materials And Mechanical Properties",
    page_icon="pictures/favicon.ico",
)

def plot_pair_plot(df):
    numeric_df = df.select_dtypes(include=np.number)
    apply_plot_settings()  # Apply the plot settings
    pair_plot = sns.pairplot(numeric_df, hue='Use', palette='husl')
    apply_axes_settings(pair_plot)  # Apply the axes settings
    st.pyplot(pair_plot)

def plot_histograms(df):
    numeric_df = df.select_dtypes(include=np.number)
    apply_plot_settings()  # Apply the plot settings

    fig, axes = plt.subplots(3, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, column in enumerate(numeric_df.columns):
        sns.histplot(numeric_df[column], kde=True, color='skyblue', stat='density', ax=axes[i])
        axes[i].set_title(column)
        axes[i].set_xlabel('Values')
        axes[i].set_ylabel('Density')
    
    apply_axes_settings(axes)  # Apply the axes settings
    
    plt.tight_layout()
    st.pyplot(fig)

def plot_box_violin_plots(df):
    if 'rating' not in df.columns or 'Su/Sy' not in df.columns:
        st.warning("The necessary feature engineering steps were not applied. Please go to the Feature engineering page and create features 'rating' and 'Su/Sy' first.")
        return

    columns_to_plot = ['Su', 'Sy', 'E', 'G', 'mu', 'Ro', 'rating', 'Su/Sy']
    apply_plot_settings()  # Apply the plot settings

    # Box plots
    fig, axes = plt.subplots(2, 4, figsize=(15, 10))
    plt.subplots_adjust(hspace=0.5)
    axes = axes.flatten()
    for i, column in enumerate(columns_to_plot):
        sns.boxplot(x=df[column], color='skyblue', ax=axes[i])
        axes[i].set_title(column)

    apply_axes_settings(axes)  # Apply the axes settings
    st.pyplot(fig)

    # Violin plots
    fig, axes = plt.subplots(2, 4, figsize=(15, 10))
    plt.subplots_adjust(hspace=0.5)
    axes = axes.flatten()
    for i, column in enumerate(columns_to_plot):
        sns.violinplot(x=df[column], color='salmon', ax=axes[i])
        axes[i].set_title(column)

    apply_axes_settings(axes)  # Apply the axes settings
    st.pyplot(fig)

def plot_pair_plot_numerical(df):
    if 'rating' not in df.columns or 'Su/Sy' not in df.columns:
        st.warning("The necessary feature engineering steps were not applied. Please go to the Feature engineering page and create features 'rating' and 'Su/Sy' first.")
        return
    apply_plot_settings()  # Apply the plot settings

    pair_plot = sns.pairplot(df, vars=['Su', 'Sy', 'E', 'G', 'mu', 'Ro', 'rating', 'Su/Sy'], kind='scatter')
    pair_plot.fig.suptitle('Pair Plot of Numerical Variables', y=1.02)

    apply_axes_settings(pair_plot)  # Apply the axes settings
    st.pyplot(pair_plot)

def plot_joint_plot(df):
    apply_plot_settings()  # Apply the plot settings

    joint_plot = sns.jointplot(data=df, x='Su', y='Sy', kind='scatter')
    plt.suptitle('Joint Plot of Su vs Sy', y=1.02)
    plt.tight_layout()
    
    st.pyplot(joint_plot)

def plot_violin_plot(df):
    apply_plot_settings()  # Apply the plot settings

    fig, ax = plt.subplots()
    sns.violinplot(data=df, inner='point', ax=ax)
    ax.set_title('Violin Plot')
    
    apply_axes_settings([ax])  # Apply the axes settings
    st.pyplot(fig)


def eda():

    # Hide Streamlit style components
    hide_streamlit_style()

    if 'df' not in st.session_state:
        st.warning("No data available. Please go to the 'Main Page' to load the data.")
        return

    df = st.session_state['df']

    st.write("## 🔍 Exploratory Data Analysis (EDA)")
    st.dataframe(df.head())


    st.write("### Pair Plot Analysis")
    if st.checkbox('Show Pair Plot'):
        st.write("""
            The pair plot is a matrix of scatter plots that shows the relationship between each pair of features in the dataset.
            This can help visualize the distributions of single variables and relationships between two variables. 
        """)
        plot_pair_plot(df)

    st.write("### Histogram Plot Analysis")
    if st.checkbox('Show Histogram Plots'):
        st.write("""
            The histogram plot shows the distribution of individual variables in the dataset.
            Each subplot displays the histogram and kernel density estimate (KDE) for a specific variable.
        """)
        plot_histograms(df)


    st.write("### Box Plot and Violin Plot Analysis")   
    if st.checkbox('Show Box and Violin Plots'):
        st.write("""
            The box plot shows the distribution of data based on a five-number summary: minimum, first quartile (Q1), median, third quartile (Q3), and maximum. 
            The violin plot combines aspects of the box plot and a kernel density plot. It provides a deeper understanding of the distribution of the data.
        """)
        plot_box_violin_plots(df)

    if st.checkbox('Show Pair Plot of Numerical Variables'):
        st.write("### Pair Plot of Numerical Variables")
        st.write("""
            The pair plot shows scatter plots of pairs of numerical variables in the dataset. It helps in visualizing the relationship between different numerical variables.
        """)
        plot_pair_plot_numerical(df)

    if st.checkbox('Show Joint Plot of Su vs Sy'):
        st.write("""
            The joint plot shows a scatter plot of two numerical variables, Su and Sy. It helps in visualizing the correlation between these two variables.
        """)
        plot_joint_plot(df)

    if st.checkbox('Show Violin Plot'):
        st.write("### Violin Plot")
        st.write("""
            The violin plot shows the distribution of a numerical variable across different categories. It combines the box plot and a kernel density plot.
        """)
        plot_violin_plot(df)

if __name__ == "__main__":
    eda()