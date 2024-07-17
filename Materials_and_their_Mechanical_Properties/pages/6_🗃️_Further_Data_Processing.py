import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from imblearn.over_sampling import SMOTE
from utils.plot_settings import apply_plot_settings, apply_axes_settings
from utils.streamlit_style import hide_streamlit_style

st.set_page_config(
    page_title="Materials And Mechanical Properties",
    page_icon="pictures/favicon.ico",
)

def scale_and_pca(df):
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df[['Su', 'Sy', 'E', 'G', 'mu']])
    pca = PCA(n_components=3)  # Choose number of principal components
    principal_components = pca.fit_transform(scaled_features)
    principal_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2', 'PC3'])
    return principal_df

def plot_principal_components(principal_df):
    apply_plot_settings()  # Apply the plot settings

    fig, ax = plt.subplots()
    sns.scatterplot(data=principal_df, x='PC1', y='PC2', ax=ax)
    ax.set_title('PCA: PC1 vs PC2')
    apply_axes_settings([ax])  # Apply the axes settings
    st.pyplot(fig)

def plot_3d_principal_components(principal_df):
    apply_plot_settings()  # Apply the plot settings

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(principal_df['PC1'], principal_df['PC2'], principal_df['PC3'], c='b', marker='o')
    ax.set_xlabel('PC1')
    ax.set_ylabel('PC2')
    ax.set_zlabel('PC3')
    ax.set_title('3D PCA Plot')

    apply_axes_settings([ax])  # Apply the axes settings
    st.pyplot(fig)

def plot_hexbin_jointplot(df):
    st.write("### Hexbin Jointplot between Su and Sy")
    st.write("This plot shows a hexbin jointplot which is useful for visualizing the relationship between two variables along with the density of data points.")

    apply_plot_settings()  # Apply the global plot settings

    jointplot = sns.jointplot(x='Su', y='Sy', data=df, kind='hex', color='blue')
    jointplot.fig.suptitle('Hexbin Jointplot between Su and Sy', y=1.03)
    st.pyplot(jointplot.fig)

def plot_residual(df):
    st.write("### Residual Plot between E and G")
    st.write("A residual plot shows the difference between observed and predicted values of data.")

    apply_plot_settings()  # Apply the global plot settings

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.residplot(x='E', y='G', data=df, scatter_kws={'s': 80}, ax=ax)
    ax.set_title('Residual Plot between E and G')

    apply_axes_settings([ax])  # Apply the axes settings

    st.pyplot(fig)

def plot_swarm(df):
    st.write("### Swarm Plot for Use vs. Rating")
    st.write("A swarm plot is useful for visualizing the distribution of a categorical variable. Note: If too many points overlap, some may not be displayed.")

    apply_plot_settings()  # Apply the global plot settings

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.swarmplot(x='Use', y='rating', hue='Use', data=df, ax=ax, size=4)  # Reduce marker size
    ax.set_title('Swarm Plot for Use vs. Rating')

    apply_axes_settings([ax])  # Apply the axes settings

    st.pyplot(fig)

def plot_kde(df):
    st.write("### KDE Plot for Young's Modulus (E) by Use")
    st.write("A KDE plot shows the distribution of a variable for different categories. Note: If too many points overlap, the density estimation might not be accurate.")

    apply_plot_settings()  # Apply the global plot settings

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.kdeplot(x=df['E'], hue=df['Use'], fill=True, ax=ax, bw_adjust=0.5)  # Adjust bandwidth
    ax.set_title("KDE Plot for Young's Modulus (E) by Use")

    apply_axes_settings([ax])  # Apply the axes settings

    st.pyplot(fig)

def plot_box(df):
    st.write("### Box Plot for Use vs. Shear Modulus (G)")
    st.write("A box plot is useful for visualizing the distribution of a variable and identifying outliers.")

    apply_plot_settings()  # Apply the global plot settings

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.boxplot(x='Use', y='G', data=df, ax=ax)
    ax.set_title('Box Plot for Use vs. Shear Modulus (G)')

    apply_axes_settings([ax])  # Apply the axes settings

    st.pyplot(fig)

def plot_pairgrid(df):
    st.write("### PairGrid Plot")

    apply_plot_settings()  # Apply the plot settings

    g = sns.PairGrid(df)
    g.map_upper(sns.scatterplot)
    g.map_diag(sns.histplot, kde=True)
    g.map_lower(sns.kdeplot)

    # Apply the axes settings to each subplot
    for ax in g.axes.flatten():
        if ax:
            apply_axes_settings([ax])

    st.pyplot(g.fig)


def plot_complex_relationships(df):
    st.write("### Complex Relationships Plot")

    apply_plot_settings()  # Apply the plot settings

    # Clustermap
    st.write("#### Correlation Clustermap")
    cluster_fig = sns.clustermap(df.corr(), cmap='coolwarm', annot=True)
    plt.setp(cluster_fig.ax_heatmap.get_xticklabels(), rotation=45)
    plt.setp(cluster_fig.ax_heatmap.get_yticklabels(), rotation=0)
    st.pyplot(cluster_fig.fig)

    # FacetGrid with scatter and kdeplot
    st.write("#### FacetGrid with Scatter and KDE Plot")
    g = sns.FacetGrid(df, col='Use', hue='Use')
    g.map_dataframe(sns.scatterplot, 'Su', 'Sy')

    # Adding KDE plot separately since it does not fit into FacetGrid
    fig, ax = plt.subplots()
    sns.kdeplot(data=df['E'], shade=True, ax=ax)
    ax.set_title("KDE Plot of Young's Modulus (E)")

    for ax in g.axes.flatten():
        if ax:
            apply_axes_settings([ax])  # Apply the axes settings

    st.pyplot(g.fig)
    st.pyplot(fig)


def resample_data_with_smote(df):
    X = df.drop(columns=['Use'])
    y = df['Use']

    oversampler = SMOTE(sampling_strategy='auto', random_state=42)
    X_resampled, y_resampled = oversampler.fit_resample(X, y)

    resampled_df = pd.DataFrame(X_resampled, columns=X.columns)
    resampled_df['Use'] = y_resampled

    return resampled_df

def further_processing():

    # Hide Streamlit style components
    hide_streamlit_style()

    if 'df_fe' not in st.session_state:
        st.warning("No data available. Please go to the 'Main Page' to load the data.")
        return

    df = st.session_state['df_fe']

    st.write("## 🗃️ Further Data Processing")


    if st.button('Perform Scaling and PCA'):

        st.write("""
            This section allows you to perform scaling and Principal Component Analysis (PCA) on the dataset.
            PCA is used to reduce the dimensionality of the dataset while retaining most of the variance.
            Use the button below to perform scaling and PCA.
        """)

        principal_df = scale_and_pca(df)
        st.write("### Principal Components DataFrame")
        st.dataframe(principal_df)
        st.session_state['principal_df'] = principal_df  # Store the principal components dataframe in session state

    if 'principal_df' in st.session_state:
        if st.checkbox('Show 2D PCA plot'):
            st.write("""
                The scatter plot below shows the first two principal components after performing PCA.
            """)
            plot_principal_components(st.session_state['principal_df'])

        if st.checkbox('Show 3D PCA plot'):
            st.write("""
                The 3D scatter plot below shows the first three principal components after performing PCA.
            """)
            plot_3d_principal_components(st.session_state['principal_df'])

            st.write("---")


    if st.checkbox("Show Hexbin Jointplot between Su and Sy"):
        plot_hexbin_jointplot(df)
    
    if st.checkbox("Show Residual Plot between E and G"):
        plot_residual(df)
    
    if st.checkbox("Show Swarm Plot for Use vs. Rating"):
        plot_swarm(df)
    
    if st.checkbox("Show KDE Plot for Young's Modulus (E) by Use"):
        plot_kde(df)
    
    if st.checkbox("Show Box Plot for Use vs. Shear Modulus (G)"):
        plot_box(df)


    # Checkbox to show the PairGrid plot
    if st.checkbox('Show PairGrid Plot'):
        st.write("""
        This plot provides a comprehensive view of the relationships between all pairs of variables in the dataset.
        """)
        plot_pairgrid(df)

    # Checkbox to show the complex relationships plot
    if st.checkbox('Show Complex Relationships Plot'):
        st.write("""
        This section includes a clustermap showing correlations between variables and a FacetGrid plot that visualizes scatter and KDE plots by categories.
        """)
        plot_complex_relationships(df)


    if st.checkbox('Resample Data with SMOTE'):
        st.write("""
            This section allows you to resample the dataset using SMOTE (Synthetic Minority Over-sampling Technique).
            SMOTE is used to address class imbalance by generating synthetic samples.
        """)
        resampled_df = resample_data_with_smote(df)
        st.write("### Resampled DataFrame")
        st.dataframe(resampled_df)
        st.write("### Value Counts of 'Use' in Resampled DataFrame")
        st.text(resampled_df["Use"].value_counts())


if __name__ == "__main__":
    further_processing()