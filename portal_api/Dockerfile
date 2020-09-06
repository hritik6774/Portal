# Use the Python3.7.2 container image
FROM python:3.8.5-alpine3.12

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install the dependencies 
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev build-base linux-headers pcre-dev libffi-dev openssl-dev
RUN pip install -r requirements.txt

# run the command to start uWSGI
CMD ["uwsgi", "uwsgi.ini"]