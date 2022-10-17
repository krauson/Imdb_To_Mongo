# download docker
# docker -v
# docker pull mongo

# Creating a container for MongoDB.
# docker create -it --name MongoTest -p 5000:27017 mongo
#
# docker start MongoTest
# docker exec -it MongoTest bash
#
#
# create an image from Dockerfile_yaniv
# docker build -t flask_app .
#
# Now that we have an image, let’s run the application
# docker run -dp 3000:3000 getting-started

# docker create -it --name app_image -p 5000:5000 app_image

# docker run -dit app

