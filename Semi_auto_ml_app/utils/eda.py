import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
import feature_engine as fe
from utils.data_utils import determine_feature_type, categorize_columns
# from feature_engine.variable_handling import check_all_variables

def styled_message(message):
    """Function to return a styled message"""
    return f"""
    <div style="background-color: #d4edda; padding: 10px; border-radius: 5px;">
        {message}
    </div>
    """



def label_encode_categorical_features(df, categorical_cols):
    """
    Label encodes categorical features in the DataFrame.

    Parameters:
    -----------
    df : pandas DataFrame
        The DataFrame containing the categorical features to be label encoded.
    
    categorical_cols : list
        List of column names that contain categorical features.
    
    Returns:
    --------
    df : pandas DataFrame
        Updated DataFrame with label encoded categorical features.
    
    label_mappings : dict
        Dictionary containing mappings of encoded labels to original values for each categorical column.
    """
    label_mappings = {}

    le = LabelEncoder()
    for col in categorical_cols:
        df[col] = le.fit_transform(df[col])
        label_mappings[col] = dict(zip(le.classes_, le.transform(le.classes_)))

    return df, label_mappings


def run_eda():

    st.subheader("Exploratory Data Analysis")
    df = st.session_state['df']
    
    numerical_discrete_cols = st.session_state['numerical_discrete_cols']
    numerical_continuous_cols = st.session_state['numerical_continuous_cols']
    categorical_cols = st.session_state['categorical_cols']

    # Display DataFrame head if available
    st.dataframe(df.head())


    if st.checkbox("Show Feature Types"):
        st.markdown(styled_message("Numerical Discrete Single Variate: 1 Unique Value \n Numerical Discrete Binary: 2 Unique Values \
            Numerical Discrete: <=10 Unique Values\n Numerical Continuous: >10 Unique Values"), unsafe_allow_html=True)

        feature_types = {
            "Feature Name": [],
            "Type": []
        }
        for col in df.columns:
            feature_type = determine_feature_type(df, col)
            if feature_type:
                feature_types["Feature Name"].append(col)
                feature_types["Type"].append(feature_type)

        st.table(pd.DataFrame(feature_types))

    # Moved parts are now in main_page.py
    if st.checkbox("Correlation Plot(Matplotlib)"):
        numeric_df = df.select_dtypes(include='number')
        fig, ax = plt.subplots()
        ax.matshow(numeric_df.corr())
        plt.xticks(range(len(numeric_df.columns)), numeric_df.columns, rotation=90)
        plt.yticks(range(len(numeric_df.columns)), numeric_df.columns)
        st.pyplot(fig)


    if st.checkbox("Correlation Plot(Seaborn)"):
        numeric_df = df.select_dtypes(include='number')
        fig, ax = plt.subplots()
        sns.heatmap(numeric_df.corr(), annot=True, ax=ax)
        st.pyplot(fig)

    if st.checkbox("Pie Plot"):
        all_columns = df.columns.to_list()
        column_to_plot = st.selectbox("Select 1 Column", all_columns)

        if df[column_to_plot].dtype == 'object':
            if df[column_to_plot].nunique() <= 30:
                fig, ax = plt.subplots()
                pie_data = df[column_to_plot].value_counts()
                ax.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%", startangle=140)
                ax.axis('equal')
                st.pyplot(fig)
            else:
                st.warning("Selected column has more than 30 categories. Displaying a table instead.")
                value_counts = df[column_to_plot].value_counts().reset_index()
                value_counts.columns = [column_to_plot, 'Count']
                st.dataframe(value_counts)
        else:
            st.write("Selected column is not categorical or discrete numerical. Please select a categorical or discrete numerical column.")

    # Initialize variables to store label encoder results
    label_enc_complete = st.session_state.get('label_enc_complete', False)
    df_encoded = st.session_state.get('df_encoded', None)
    label_mappings = st.session_state.get('label_mappings', None)

    # Button to trigger label encoding
    if not label_enc_complete:
        if st.button('Run Label Encoder'):
            df_encoded, label_mappings = label_encode_categorical_features(df.copy(), categorical_cols)
            st.session_state['label_enc_complete'] = True  # Mark label encoding as complete
            st.session_state['df_encoded'] = df_encoded  # Store encoded DataFrame in session state
            st.session_state['label_mappings'] = label_mappings  # Store label mappings in session state
            st.experimental_rerun()  # Rerun to update the UI
    else:
        st.markdown("""
            <style>
            .css-1cpxqw2 {
                pointer-events: none;
                opacity: 0.6;
                background-color: #a9a9a9 !important;
            }
            </style>
            """, unsafe_allow_html=True)
        st.button('Run Label Encoder')

    # Show label encoder results if encoding is complete
    if st.session_state.get('label_enc_complete', False):
        if st.checkbox("Show Label Encoder Results"):
            df_encoded = st.session_state['df_encoded']
            label_mappings = st.session_state['label_mappings']
            formatted_results = {
                'Feature': [],
                'Encoded Values': [],
                'Original Values': []
            }
            for col in categorical_cols:
                encoded_values = list(df_encoded[col].unique())
                original_values = list(label_mappings[col].keys())
                formatted_results['Feature'].append(col)
                formatted_results['Encoded Values'].append(encoded_values)
                formatted_results['Original Values'].append(original_values)

            if len(formatted_results['Feature']) > 10:  # Limiting to 10 rows for demonstration
                st.table(pd.DataFrame(formatted_results).head(10))
                st.write(f"Showing first 10 rows out of {len(formatted_results['Feature'])} total rows.")
            else:
                st.table(pd.DataFrame(formatted_results))

