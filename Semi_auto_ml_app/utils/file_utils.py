def writetofile(text,file_name):
	with open(os.path.join('downloads',file_name),'w') as f:
		f.write(text)

def download_file():
	file_name = "model_results.json"
	with open(os.path.join('downloads', file_name), 'r') as f:
		result_to_file = f.read()
		
	b64 = base64.b64encode(result_to_file.encode()).decode()
	href = f'<a href="data:file/json;base64,{b64}" download="{file_name}">Download {file_name}</a>'
	st.markdown(href, unsafe_allow_html=True)