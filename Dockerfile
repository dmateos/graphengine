# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory to /app
WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libssl-dev locales locales-all

# Install any needed packages specified in requirements.txt
COPY . /app/
RUN pip install -r /app/requirements.txt

# Try to run your service on port 8080 if possible
EXPOSE 8080

# Dont bother to change this line.
# This is overridden by the azure runner of the container on deployment.
CMD "/app/worker_start.sh"
