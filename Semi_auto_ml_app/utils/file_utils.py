import os
import json
import base64
import pandas as pd
import streamlit as st

def writetofile(text,file_name):
	with open(os.path.join('downloads',file_name),'w') as f:
		f.write(text)

def download_file(data, file_name):
    # Convert data to JSON string
    result_to_file = json.dumps(data, indent=4)

    # Create a BytesIO object to hold the bytes of the file
    b64 = base64.b64encode(result_to_file.encode()).decode()

    # Generate download link
    href = f'<a href="data:file/json;base64,{b64}" download="{file_name}">Download {file_name}</a>'
    return href

# Function to load dataset from file uploader or predefined folder
def load_dataset():
    # Check if datasets folder exists
    if not os.path.exists('datasets'):
        os.makedirs('datasets')

    # Ask user for initial choice: Upload or Select (on the sidebar)
    choice = st.sidebar.radio("Choose an option:", ("Upload a Dataset", "Select from Server"))

    if choice == "Upload a Dataset":
        uploaded_data = st.sidebar.file_uploader("Upload a Dataset", type=["csv", "txt"])
        if uploaded_data is not None:
            df = pd.read_csv(uploaded_data)
            st.sidebar.success("Dataset uploaded successfully.")
            return df
        else:
            st.info("Please upload a dataset to proceed.")
            return None

    elif choice == "Select from Server":
        # List datasets in the folder
        datasets_list = os.listdir('datasets')

        if not datasets_list:
            st.sidebar.info("No datasets found on the server.")
            return None

        selected_dataset = st.sidebar.selectbox("Select a Dataset", datasets_list)
        if selected_dataset:
            st.info(f"Dataset '{selected_dataset}' selected. Confirm selection in the sidebar to proceed.")
            return selected_dataset  # Return the dataset name for confirmation

        return None