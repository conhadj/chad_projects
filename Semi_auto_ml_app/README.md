Drag & Drop Semi Auto ML

Overview

The "Drag & Drop Semi Auto ML" application is a user-friendly tool for performing machine learning tasks without coding. Built using Streamlit, this app allows users to upload datasets, conduct Exploratory Data Analysis (EDA), visualize data, and build machine learning models. The application is designed to streamline the data analysis process, making it accessible for users with minimal levels of programming experience.

Features

Exploratory Data Analysis (EDA):

- Upload datasets in CSV or TXT format.
- Display the first few rows of the dataset.
- Show the shape and column names of the dataset.
- Provide statistical summaries of the data.
- Select and display specific columns.
- Show value counts of the target column.
- Generate correlation plots using Matplotlib and Seaborn.
- Create pie charts for categorical data.

Data Visualization:

- Upload datasets and display the first few rows.
- Display value counts of the target column using bar plots.
- Generate customizable plots (area, bar, line, histograms, box plots, and KDE plots) for selected columns.

Model Building:

- Upload datasets and sample large datasets.
- Select the output column (target variable) and determine its type.
- Handles automatically missing values by imputing numeric and categorical data.
- Encodes automatically categorical columns.
- Select and train multiple machine learning models (classification and regression).
- Display model performance metrics (mean accuracy and standard deviation) in table or JSON format.
- Save and download model results as a JSON file.

Usage

Access the Application

The app is deployed on Google Cloud Platform (GCP). 

You can access it directly using the following link:

https://streamlit-ml-app.nw.r.appspot.com/

----------------------------------------------------------------------------------------------------

What is Streamlit?

Streamlit is an open-source Python library that makes it easy to create and share beautiful, custom web apps for machine learning and data science. It allows developers to transform data scripts into interactive, shareable web applications in just a few lines of code. Streamlit's simplicity and flexibility make it a popular choice for rapid prototyping and developing data-driven applications.