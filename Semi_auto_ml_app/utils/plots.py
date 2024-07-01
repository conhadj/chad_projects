import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_null_heatmap(df):
    """Function to plot null value heatmap using Seaborn"""
    st.subheader("Null Value Heatmap")
    plt.figure(figsize=(10, 6))
    sns.heatmap(df.isnull(), cbar=False, cmap='viridis', yticklabels=False)
    st.pyplot()

def styled_message(message):
    """Function to return a styled message"""
    return f"""
    <div style="background-color: #d4edda; padding: 10px; border-radius: 5px;">
        {message}
    </div>
    """

def plot_numerical_feature(df, selected_feature):
    """Function to plot a selected numerical feature using Seaborn"""
    st.subheader(f"Plot for {selected_feature}")
    fig, ax = plt.subplots()
    sns.histplot(df[selected_feature], kde=True, ax=ax)
    st.pyplot(fig)

def plot_box_plots(df, selected_features):
    """Function to plot box plots for selected numerical features using Seaborn"""
    st.subheader("Box Plots for Selected Features")
    fig, ax = plt.subplots(figsize=(30, 10))
    sns.boxplot(data=df[selected_features], ax=ax)
    ax.set_title("Box Plots")
    st.pyplot(fig)

def plot_area_chart(df, selected_columns):
    """Function to plot area chart for selected columns"""
    st.success(f"Generating Customizable Plot of area chart for {selected_columns}")
    st.area_chart(df[selected_columns])

def plot_bar_chart(df, selected_columns):
    """Function to plot bar chart for selected columns"""
    st.success(f"Generating Customizable Plot of bar chart for {selected_columns}")
    st.bar_chart(df[selected_columns])

def plot_line_chart(df, selected_columns):
    """Function to plot line chart for selected columns"""
    st.success(f"Generating Customizable Plot of line chart for {selected_columns}")
    st.line_chart(df[selected_columns])

def plot_kde_plot(df, selected_columns):
    """Function to plot KDE plot for selected columns"""
    st.success(f"Generating Customizable Plot of KDE plot for {selected_columns}")
    fig, ax = plt.subplots()
    df[selected_columns].plot(kind='kde', ax=ax)
    st.pyplot(fig)

def run_plots():
    st.subheader("Data Visualization")
    df = st.session_state['df']

    if st.checkbox("Show Value Counts"):
        fig, ax = plt.subplots()
        df.iloc[:, -1].value_counts().plot(kind='bar', ax=ax)
        st.pyplot(fig)

    all_columns_names = df.columns.tolist()
    type_of_plot = st.selectbox("Select Type of Plot", ["area", "bar", "line", "hist", "box", "kde"])
    
    if type_of_plot in ['hist', 'box', 'kde']:
        # Filter numeric columns only for histogram, box plot, and KDE plot
        available_columns = df.select_dtypes(include='number').columns.tolist()
    else:
        # Show all columns for area, bar, and line charts
        available_columns = all_columns_names
    
    selected_columns_names = st.multiselect("Select Columns To Plot", available_columns)

    if st.button("Generate Plot"):
        if type_of_plot in ["area", "bar", "line"]:
            if selected_columns_names:
                if type_of_plot == 'area':
                    plot_area_chart(df, selected_columns_names)
                elif type_of_plot == 'bar':
                    plot_bar_chart(df, selected_columns_names)
                elif type_of_plot == 'line':
                    plot_line_chart(df, selected_columns_names)
            else:
                st.warning("Please select at least one column to plot.")
        
        elif type_of_plot == 'hist':
            if not selected_columns_names:
                st.warning("Please select at least one numeric column for the histogram plot.")
            else:
                st.success(f"Generating Customizable Plot of {type_of_plot} for {selected_columns_names}")
                fig, ax = plt.subplots()
                df[selected_columns_names].plot(kind='hist', bins=30, alpha=0.5, ax=ax)
                st.pyplot(fig)
        
        elif type_of_plot == 'box':
            if not selected_columns_names:
                st.warning("Please select at least one numeric column for the box plot.")
            else:
                plot_box_plots(df, selected_columns_names)
        
        elif type_of_plot == 'kde':
            if not selected_columns_names:
                st.warning("Please select at least one numeric column for the KDE plot.")
            else:
                plot_kde_plot(df, selected_columns_names)