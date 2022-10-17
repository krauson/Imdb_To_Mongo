# todo : template for creating python web server image

# step 1 select default OS Image
FROM alpine

# Defining working directory
WORKDIR /posters_app

# Step 2 Setting up environment
RUN apk update
RUN apk add --no-cache python3-dev && apk add py3-pip
RUN pip install --upgrade pip

# step 3 Configure a software

# Exposing an internal port
EXPOSE 80

# Installing dependencies
COPY . .


RUN pip install -r requirements.txt

# Copying project files
RUN mkdir -p /app/{templates}



# step 4 set default commands
# Default command
ENTRYPOINT ["python3"]

# These commands will be replaced if user provides any command by himself
CMD ["app.py"]
