# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster
#set the working directory in the container
WORKDIR /app

COPY requirements.txt requirements.txt

#copy current directories 
COPY . ./app

# Install dependencies
RUN pip install -r requirements.txt

# Define environment variable
ENV FLASK_APP=app.py

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]