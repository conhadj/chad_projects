import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder


def run_preprocess():
    st.subheader("Data Visualization")
    
    # Check if 'df' is in session state
    if 'df' not in st.session_state:
        st.error("No dataset found. Please upload a dataset on the main page.")
        return

    df = st.session_state['df']

    # Check and initialize other necessary session state variables
    if 'label_enc_complete' not in st.session_state:
        st.session_state['label_enc_complete'] = False
    if 'df_encoded' not in st.session_state:
        st.session_state['df_encoded'] = None
    if 'label_mappings' not in st.session_state:
        st.session_state['label_mappings'] = None

    # Verify if categorical columns are correctly identified
    if 'categorical_cols' not in st.session_state:
        st.error("Categorical columns not identified. Please categorize columns on the main page.")
        return

    numerical_discrete_cols = st.session_state['numerical_discrete_cols']
    numerical_continuous_cols = st.session_state['numerical_continuous_cols']
    categorical_cols = st.session_state['categorical_cols']


    # Multiselect box and button to drop selected features
    features_to_drop = st.multiselect('Select features to drop', df.columns)
    if st.button('Drop features'):
        if features_to_drop:
            df.drop(columns=features_to_drop, inplace=True)
            st.success(f"You dropped columns: {', '.join(features_to_drop)}")

            # Update session state with modified dataframe
            st.session_state['df'] = df

            # Update numerical and categorical columns lists
            st.session_state['numerical_discrete_cols'] = [col for col in numerical_discrete_cols if col not in features_to_drop]
            st.session_state['numerical_continuous_cols'] = [col for col in numerical_continuous_cols if col not in features_to_drop]
            st.session_state['categorical_cols'] = [col for col in categorical_cols if col not in features_to_drop]

    # Button to trigger label encoding
    if not st.session_state['label_enc_complete']:
        if st.button('Run Label Encoder'):
            df_encoded, label_mappings = label_encode_categorical_features(df.copy(), categorical_cols)
            st.session_state['label_enc_complete'] = True  # Mark label encoding as complete
            st.session_state['df_encoded'] = df_encoded  # Store encoded DataFrame in session state
            st.session_state['label_mappings'] = label_mappings  # Store label mappings in session state
            st.experimental_rerun()  # Rerun to update the UI

    # Show label encoder results if encoding is complete
    if st.session_state['label_enc_complete']:
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

        df_encoded = st.session_state['df_encoded']
        label_mappings = st.session_state['label_mappings']

        # Debugging: print categorical columns
        st.write("Categorical Columns:")
        st.write(categorical_cols)

        st.write("Encoded DataFrame:")
        st.dataframe(df_encoded.head())
        
        st.write("Label Mappings:")
        st.json(label_mappings)

        formatted_results = {
            'Feature': [],
            'Encoded Values': [],
            'Original Values': []
        }
        for col in df_encoded.columns:
            if col in label_mappings:
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


def label_encode_categorical_features(df, categorical_cols):
    df_encoded = df.copy()
    label_mappings = {}

    for col in categorical_cols:
        if col in df.columns:
            if df[col].dtype == 'object' or df[col].dtype.name == 'category':
                le = LabelEncoder()
                df_encoded[col] = le.fit_transform(df_encoded[col])
                label_mappings[col] = dict(zip(le.classes_, le.transform(le.classes_)))
            else:
                st.write(f"Column {col} is not categorical and will not be encoded.")
                df_encoded.drop(col, axis=1, inplace=True)  # Drop non-categorical columns
        else:
            st.write(f"Column '{col}' not found in the DataFrame.")
            
    return df_encoded, label_mappings