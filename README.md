# Imdb_To_Mongo
Project Description:

This project aims to use web browser to download a chosen movie poster,
the software first start looking at a designated MongoDB if the poster is not found there,
the software tries to download it from IMDB through API request using API key,
after downloading the poster from IMDB to the local computer the poster is inserted to MongoDB,
so the next time the very same poster will be requested it will be retrieved from MongoDB,
which will be faster.

Action to do for using the app:
1)pip install -r requirements.txt (download all the dependencies for this project).
2)make sure you have posters folder in the location you run app_server from.
3)run the file app_server.py using.
4)open the browser and choose your prefered movie.


Right now the config_file.py have to be transfered manually into the EC2.
