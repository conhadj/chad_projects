import json
import base64

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