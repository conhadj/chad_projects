import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from utils.data_utils import sample_dataframe, determine_feature_type


def run_preprocess():
    st.subheader("Data preprocessing")
    
    # Check if 'df' is in session state
    if 'df' not in st.session_state:
        st.error("No dataset found. Please upload a dataset on the main page.")
        return

    # Sample the dataframe if it's too large
    df = sample_dataframe(st.session_state['df'])

    # Initialize variables to store label encoder results
    label_enc_complete = st.session_state.get('label_enc_complete', False)
    df_encoded = st.session_state.get('df_encoded', None)
    label_mappings = st.session_state.get('label_mappings', None)

    # Multiselect box and button to drop selected features
    features_to_drop = st.multiselect('Select features to drop', df.columns)
    if st.button('Drop features'):
        if features_to_drop:
            df.drop(columns=features_to_drop, inplace=True)
            st.success(f"You dropped columns: {', '.join(features_to_drop)}")

            # Update lists by removing the dropped columns
            st.session_state['numerical_discrete_cols'] = [col for col in st.session_state['numerical_discrete_cols'] if col not in features_to_drop]
            st.session_state['numerical_continuous_cols'] = [col for col in st.session_state['numerical_continuous_cols'] if col not in features_to_drop]
            st.session_state['categorical_cols'] = [col for col in st.session_state['categorical_cols'] if col not in features_to_drop]

            # Update session state with modified dataframe
            st.session_state['df'] = df

    st.markdown("----")

    # Button to trigger label encoding
    if not label_enc_complete:
        if st.button('Run Label Encoder'):
            df_encoded, label_mappings = label_encode_categorical_features(df.copy(), st.session_state['categorical_cols'])
            st.session_state['label_enc_complete'] = True  # Mark label encoding as complete
            st.session_state['df_encoded'] = df_encoded  # Store encoded DataFrame in session state
            st.session_state['label_mappings'] = label_mappings  # Store label mappings in session state
            st.experimental_rerun()  # Rerun to update the UI

    # Show label encoder results if encoding is complete
    if label_enc_complete:
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

        # Debugging: print categorical columns
        st.write("Categorical Columns:")
        st.write(st.session_state['categorical_cols'])

        if st.checkbox("Show Encoded Dataframe"):
            st.write("Encoded DataFrame:")
            st.dataframe(df_encoded.head())

        if st.checkbox("Show Label Mappings in a Table"):
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

        if st.checkbox("Show Label Mappings (JSON format)"):
            st.json(label_mappings)

    st.markdown("----")

    if st.button("Handle Missing Values"):
        # Handle missing values
        missing_info = df.isnull().sum()
        columns_with_missing = missing_info[missing_info > 0].index.tolist()
        if columns_with_missing:
            st.write("Columns with missing values and the count of missing values:")
            st.write(missing_info[missing_info > 0])


            categorical_cols = st.session_state['categorical_cols']
            # Combine numerical columns
            numeric_cols = st.session_state['numerical_discrete_cols'] + st.session_state['numerical_continuous_cols']

            # Define imputers
            num_imputer = SimpleImputer(strategy='mean')
            cat_imputer = SimpleImputer(strategy='most_frequent')

            # Apply imputers to df
            df[numeric_cols] = num_imputer.fit_transform(df[numeric_cols])
            df[categorical_cols] = cat_imputer.fit_transform(df[categorical_cols])

            # Check if label encoding is complete and df_encoded is not None
            if  label_enc_complete and df_encoded is not None:
                # Apply imputers to df_encoded
                df_encoded[numeric_cols] = num_imputer.transform(df_encoded[numeric_cols])
                df_encoded[categorical_cols] = cat_imputer.transform(df_encoded[categorical_cols])

            st.write(f"Missing values were handled: Numeric columns were filled with mean values, and categorical columns were filled with the most frequent values.")
        else:
            st.write(f"Dataset has no missing values. Therefore, no operation was performed.")

    # Update session state with modified dataframe
    st.session_state['df'] = df

    # Update numerical and categorical columns lists
    st.session_state['numerical_discrete_cols'] = [col for col in df.columns if determine_feature_type(df, col) == 'Numerical Discrete']
    st.session_state['numerical_continuous_cols'] = [col for col in df.columns if determine_feature_type(df, col) == 'Numerical Continuous']
    st.session_state['categorical_cols'] = [col for col in df.columns if determine_feature_type(df, col) == 'Categorical']


def label_encode_categorical_features(df, categorical_cols):
    df_encoded = df.copy()
    label_mappings = {}

    for col in categorical_cols:
        le = LabelEncoder()
        df_encoded[col] = le.fit_transform(df_encoded[col])
        label_mappings[col] = dict(zip(le.classes_, le.transform(le.classes_)))
            
    return df_encoded, label_mappings