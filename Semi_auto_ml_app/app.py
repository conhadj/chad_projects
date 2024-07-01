import streamlit as st
from utils.eda import run_eda
from utils.plots import run_plots
from utils.model_building import run_model_building

# App name
st.title("Drag & Drop Semi Auto ML")

def main():
	"""Semi Automated ML App with Streamlit """
	activities = ["EDA", "Plots", "Model Building", "About"]
	choice = st.sidebar.selectbox("Select Activities", activities)

	if choice == 'EDA':
		run_eda()
	elif choice == 'Plots':
		run_plots()
	elif choice == 'Model Building':
		run_model_building()
	elif choice == 'About':
		st.subheader("About")
		st.write("Constantinos Hadjigregoriou")
		st.write("constantinos.hadjigregoriou@outlook.com")

if __name__ == '__main__':
	main()