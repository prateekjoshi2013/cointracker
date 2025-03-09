# Step 1: Use an official Python runtime as the base image
FROM python:3.9-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the requirements.txt file into the container
COPY requirements.txt .

# Step 4: Install the dependencies specified in requirements.txt
RUN apt update && \
    apt install curl -y && \
    pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the entire app code into the container
COPY . .

