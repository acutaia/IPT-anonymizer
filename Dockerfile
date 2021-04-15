# Set base image (host OS)
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /ipt_anonymizer

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN apt-get update && apt-get install gcc -y && apt-get clean
RUN pip3 install --no-cache-dir -r requirements.txt



# Copy content of the application
COPY app/ ./app
COPY static/ ./static
COPY .env .
COPY server.py .
COPY setup.py .
COPY setup_database.py .

# Build c extention
RUN python3 setup.py build_ext --inplace

# Setup the Database
RUN python3 setup_database.py

# command to run on container start
CMD [ "python3", "./server.py" ]