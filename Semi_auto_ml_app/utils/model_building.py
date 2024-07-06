import streamlit as st
import pandas as pd
import json
from sklearn.model_selection import KFold, cross_val_score
from utils.data_utils import sample_dataframe, check_variable_type
from utils.file_utils import writetofile, download_file
from utils.model_utils import get_models  # Import your get_models function from model_utils.py
from utils.data_utils import sample_dataframe, determine_feature_type

def run_model_building():
    st.subheader("Building ML Models")
    
    # Check if 'df' is in session state
    if 'df' not in st.session_state:
        st.error("No dataset found. Please upload a dataset on the main page.")
        return

    df = st.session_state['df']

    # Sample the dataframe if it's too large
    df = sample_dataframe(df)

    # Select output column (Y)
    output_col = st.selectbox("Select Output Column", df.columns)

    # Determine output type before label encoding
    output_type_before_encoding = determine_feature_type(df, output_col)
    st.write(f"Output Type (Before Encoding): {output_type_before_encoding}")

    # Define ordinal data and ask user if the data is ordinal
    if output_type_before_encoding == 'Categorical' or output_type_before_encoding == 'Numerical Discrete Binary' or output_type_before_encoding == 'Numerical Discrete' :
        st.markdown("**Ordinal Data Definition:** Ordinal data is a type of categorical data with a set order or scale to it. For example, rankings, levels, and sizes (small, medium, large).")
        is_ordinal = st.selectbox("Is the data ordinal?", ["Yes", "No"])
    else:
        is_ordinal = "No"

    # Determine output type after label encoding
    output_type_after_encoding = check_variable_type(df[output_col])
    st.write(f"Output Type (After Encoding): {output_type_after_encoding}")

    # Get models based on output type and ordinality (if applicable)
    models, removed_models = get_models(output_type_after_encoding, is_ordinal)

    # Display appropriate and removed models with checkboxes
    st.write("Select models to train:")
    selected_models = []
    for model_name, model in models:
        if st.checkbox(model_name, value=True):
            selected_models.append((model_name, model))

    st.write("Models not appropriate:")
    for model_name, reason in removed_models:
        st.checkbox(model_name + " - " + reason, value=False, disabled=True)

    if st.checkbox("Train Selected Models"):
        X = df.drop(columns=[output_col])
        Y = df[output_col]

        model_names = []
        model_mean = []
        model_std = []
        all_models = []
        scoring = 'accuracy' if output_type_after_encoding != 'Numerical Continuous' else 'r2'

        # Initialize progress bar
        progress_bar = st.progress(0)

        total_models = len(selected_models)

        for i, (name, model) in enumerate(selected_models):
            try:
                kfold = KFold(n_splits=10)
                cv_results = cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
                model_names.append(name)
                model_mean.append(cv_results.mean())
                model_std.append(cv_results.std())

                accuracy_results = {"model name": name, "model_accuracy": cv_results.mean(), "standard deviation": cv_results.std()}
                print(accuracy_results)
                all_models.append(accuracy_results)

                # Update the progress bar
                progress_bar.progress((i + 1) / total_models)

            except ValueError as e:
                st.error(f"Error occurred for model {name}: {str(e)}")
                st.warning(f"Skipping model {name} due to the error.")

        # After loop completes, clear the progress bar
        progress_bar.empty()

        # Display metrics as table
        if st.checkbox("Metrics As Table"):
            st.dataframe(pd.DataFrame(zip(model_names, model_mean, model_std), columns=["Algorithm", "Mean of Accuracy", "Std"]))

        # Display metrics as JSON
        if st.checkbox("Metrics As JSON"):
            st.json(all_models)

        # Save results button
        if st.button("Save Model Results"):
            result_to_file = json.dumps(all_models)
            file_name = "model_results.json"
            writetofile(result_to_file, file_name)
            st.info(f"Saved Result As: {file_name}")
            download_file()

