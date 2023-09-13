# Use the official Python image as the base image
FROM python:3.10

#Copy requirements file into image
COPY ./requirements.txt /app/requirements.txt

#Switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

#Expose port 80
EXPOSE 80

# Define environment variable for Flask
ENV FLASK_APP=app.py

# Run the command to start the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]