# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Streamlit runs on (default is 8501)
EXPOSE 8080

# Set the default command to your app.py
CMD ["streamlit", "run",  "🏠_Main.py", "--server.port=8080", "--server.enableCORS=false"]