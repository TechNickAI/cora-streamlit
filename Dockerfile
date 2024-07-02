# Use the official Python image with the specified version
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements/requirements.txt requirements/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements/requirements.txt

# Install ffmpeg for audio input
RUN apt-get update && apt-get install -y ffmpeg

# Copy the rest of the application code into the container
COPY . .

# Expose the port that Streamlit will run on
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "Cora.py"]
