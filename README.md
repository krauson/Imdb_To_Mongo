# Imdb_To_Mongo
![alt text](https://qph.cf2.quoracdn.net/main-qimg-70b6a8ad21a92693ab61107591e4fa25-lq)
Project Description:

This project aims to use web browser to download a chosen movie poster,
the software first start looking at a designated MongoDB if the poster is not found there,
the software tries to download it from IMDB through API request using API key,
after downloading the poster from IMDB to the local computer the poster is inserted to MongoDB,
so the next time the very same poster will be requested it will be retrieved from MongoDB,
which will be faster.

Action to do for using the app:
1.Launch an EC2, use the user_data.sh file
2.Copy the config_file.py into the posters_app dir

# Right now the config_file.py have to be transfered manually into the EC2.

3.In the terminal write: docker-compose down
4.In the terminal write: docker-compose up

# (now the config_file will be taken into account as well).

5.open the browser and choose your prefered movie.
