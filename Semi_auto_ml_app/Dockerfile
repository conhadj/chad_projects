# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# (you may adjust this depending on your actual dependencies)
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Streamlit runs on (default is 8501)
EXPOSE 8501

# Set the entry point to run Streamlit
ENTRYPOINT ["streamlit", "run"]

# Set the default command to your app.py
CMD ["app.py"]