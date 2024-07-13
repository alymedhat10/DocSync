# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the credentials file into the container
COPY Key/tokyo-country-189103-4ce23189dd39.json /app/Key/tokyo-country-189103-4ce23189dd39.json

# Verify the key file exists
RUN ls -l /app/Key/tokyo-country-189103-4ce23189dd39.json

# Install required system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Google Cloud SDK
RUN wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-390.0.0-linux-x86_64.tar.gz && \
    tar -xf google-cloud-sdk-390.0.0-linux-x86_64.tar.gz && \
    ./google-cloud-sdk/install.sh && \
    rm google-cloud-sdk-390.0.0-linux-x86_64.tar.gz

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PROJECT_ID tokyo-country-189103
ENV GOOGLE_APPLICATION_CREDENTIALS /app/Key/tokyo-country-189103-4ce23189dd39.json
ENV PATH $PATH:/app/google-cloud-sdk/bin

# Expose the Streamlit port
EXPOSE 8501

# Run the app
CMD gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS && \
    gcloud services enable compute.googleapis.com aiplatform.googleapis.com storage.googleapis.com bigquery.googleapis.com --project $PROJECT_ID && \
    streamlit run app.py --server.address 0.0.0.0
