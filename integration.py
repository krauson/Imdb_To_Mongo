import logging

from tmbd_download_image import TMDBDownloader
from db_crud import MongoDB
from config_file import content_path


# logging.basicConfig(level=logging.DEBUG)


def get_poster_from_tmdb_website(tmdb, mongo_db):
    # download_poster
    filename = tmdb.download_poster_file()
    # be assigned only after using the method download_poster_file
    poster_path = tmdb.content_path + '//' + filename
    print(f"Movie {tmdb.movie_name} poster was downloaded from TMDB web API to the posters directory")
    mongo_db.write_image_file(tmdb.movie_name, poster_path, tmdb.imdb_id)
    # todo
    # run the code from app server see if get_poster_from_tmdb_website works

def get_poster_from_server_db(mongo_db, movie_name):
    mongo_db.download_file_from_db(filename=movie_name,
                                   target_location=content_path)
    print(f"Movie {movie_name} poster was downloaded from server DB to the posters directory")


def download_poster_to_user_pc(movie_name):
    """Gets a movie name and download the poster to the user's PC"""
    mongo_db = MongoDB("127.0.0.1", 27017, movie_name)
    tmdb = TMDBDownloader(movie_name)
    filename_prefix = tmdb.movie_name + "_poster"

    is_poster_in_db = mongo_db.is_filename_exist(filename_prefix)

    logging.debug(f"is poster in db:{is_poster_in_db}")
    if is_poster_in_db:
        get_poster_from_server_db(mongo_db, movie_name)

    else:
        get_poster_from_tmdb_website(tmdb, mongo_db)
