# Core Pkgs
import streamlit as st 
import os
import base64

# Time Pkg
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

# Templates
file_name = 'yourdocument' + timestr + '.txt'
HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""


# EDA Pkgs
import pandas as pd 
import numpy as np 
import time,json

# Data Viz Pkg
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use("Agg")
import seaborn as sns 


# ML Packages
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC


# ML Packages For Vectorization of Text For Feature Extraction
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer


def writetofile(text,file_name):
	with open(os.path.join('downloads',file_name),'w') as f:
		f.write(text)

def make_downloadable(filename):
	readfile = open(os.path.join("downloads",filename)).read()
	b64 = base64.b64encode(readfile.encode()).decode()
	href = '<a href="data:file/readfile;base64,{}">Download File File</a> (right-click and save as &lt;some_name&gt;.txt)'.format(b64)
	return href



def main():
	"""Semi Automated ML App with Streamlit """

	activities = ["EDA","Plots","Model Building","About"]	
	choice = st.sidebar.selectbox("Select Activities",activities)

	if choice == 'EDA':
		st.subheader("Exploratory Data Analysis")

		data = st.file_uploader("Upload a Dataset", type=["csv", "txt"])
		if data is not None:
			df = pd.read_csv(data)
			st.dataframe(df.head())

			if st.checkbox("Show Shape"):
				st.write(df.shape)

			if st.checkbox("Show Columns"):
				all_columns = df.columns.to_list()  # Initialize all_columns here
				st.write(all_columns)

			if st.checkbox("Summary"):
				st.write(df.describe())

			if st.checkbox("Show Selected Columns"):
				if 'all_columns' not in locals():  # Check if all_columns is initialized
					st.warning("Please select 'Show Columns' first to initialize column list.")
				else:
					selected_columns = st.multiselect("Select Columns", all_columns)
					new_df = df[selected_columns]
					st.dataframe(new_df)

			if st.checkbox("Show Value Counts"):
				st.write(df.iloc[:,-1].value_counts())

			if st.checkbox("Correlation Plot(Matplotlib)"):
				numeric_df = df.select_dtypes(include='number')  # Select only numeric columns
				fig, ax = plt.subplots()
				ax.matshow(numeric_df.corr())
				plt.xticks(range(len(numeric_df.columns)), numeric_df.columns, rotation=90)
				plt.yticks(range(len(numeric_df.columns)), numeric_df.columns)
				st.pyplot(fig)

			if st.checkbox("Correlation Plot(Seaborn)"):
				numeric_df = df.select_dtypes(include='number')  # Select only numeric columns
				fig, ax = plt.subplots()
				sns.heatmap(numeric_df.corr(), annot=True, ax=ax)
				st.pyplot(fig)

			if st.checkbox("Pie Plot"):
				all_columns = df.columns.to_list()
				column_to_plot = st.selectbox("Select 1 Column", all_columns)

				# Create a Matplotlib figure and axis
				fig, ax = plt.subplots()
				pie_data = df[column_to_plot].value_counts()
				ax.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%", startangle=140)
				ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

				# Display the plot using st.pyplot(fig)
				st.pyplot(fig)




	elif choice == 'Plots':
		st.subheader("Data Visualization")
		data = st.file_uploader("Upload a Dataset", type=["csv", "txt"])
		if data is not None:
			df = pd.read_csv(data)
			st.dataframe(df.head())


			if st.checkbox("Show Value Counts"):
				st.write(df.iloc[:,-1].value_counts().plot(kind='bar'))
				st.pyplot()
		
			# Customizable Plot

			all_columns_names = df.columns.tolist()
			type_of_plot = st.selectbox("Select Type of Plot",["area","bar","line","hist","box","kde"])
			selected_columns_names = st.multiselect("Select Columns To Plot",all_columns_names)

			if st.button("Generate Plot"):
				st.success("Generating Customizable Plot of {} for {}".format(type_of_plot,selected_columns_names))

				# Plot By Streamlit
				if type_of_plot == 'area':
					cust_data = df[selected_columns_names]
					st.area_chart(cust_data)

				elif type_of_plot == 'bar':
					cust_data = df[selected_columns_names]
					st.bar_chart(cust_data)

				elif type_of_plot == 'line':
					cust_data = df[selected_columns_names]
					st.line_chart(cust_data)

				# Custom Plot 
				elif type_of_plot:
					cust_plot= df[selected_columns_names].plot(kind=type_of_plot)
					st.write(cust_plot)
					st.pyplot()


	elif choice == 'Model Building':
		st.subheader("Building ML Models")
		data = st.file_uploader("Upload a Dataset", type=["csv", "txt"])
		if data is not None:
			df = pd.read_csv(data)
			st.dataframe(df.head())


			# Model Building
			X = df.iloc[:,0:-1] 
			Y = df.iloc[:,-1]
			seed = 7
			# prepare models
			models = []
			models.append(('LR', LogisticRegression()))
			models.append(('LDA', LinearDiscriminantAnalysis()))
			models.append(('KNN', KNeighborsClassifier()))
			models.append(('CART', DecisionTreeClassifier()))
			models.append(('NB', GaussianNB()))
			models.append(('SVM', SVC()))
			# evaluate each model in turn
			
			model_names = []
			model_mean = []
			model_std = []
			all_models = []
			scoring = 'accuracy'
			for name, model in models:
				#kfold = model_selection.KFold(n_splits=10, random_state=seed)
				kfold = model_selection.KFold(n_splits=10)
				cv_results = model_selection.cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
				model_names.append(name)
				model_mean.append(cv_results.mean())
				model_std.append(cv_results.std())
				
				accuracy_results = {"model name":name,"model_accuracy":cv_results.mean(),"standard deviation":cv_results.std()}
				all_models.append(accuracy_results)


			if st.checkbox("Metrics As Table"):
				st.dataframe(pd.DataFrame(zip(model_names,model_mean,model_std),columns=["Algo","Mean of Accuracy","Std"]))

			if st.checkbox("Metrics As JSON"):
				st.json(all_models)

				if st.button("Save Model Results"):
					result_to_file =json.dumps(all_models)
					writetofile(result_to_file,file_name)
					st.info("Saved Result As :: {}".format(file_name))
	
			# files = os.listdir(os.path.join('downloads'))
			# 		file_to_download = st.selectbox("Select File To Download",files)
			# 		st.info("File Name: {}".format(file_to_download))
			# 		d_link = make_downloadable(file_to_download)
			# 		st.markdown(d_link,unsafe_allow_html=True)


	elif choice == 'About':
		st.subheader("About")
		st.write("Constantinos Hadjigregoriou")
		st.write("constantinos.hadjigregoriou@outlook.com")





if __name__ == '__main__':
	main()