# import logging
from tmbd_download_image import TMDBDownloader, is_movie_exist_in_tmdb
from mongo_funcs import MongoDB, is_file_exist_in_mongo


# logging.basicConfig(level=logging.DEBUG)


def get_poster_from_tmdb_website(movie_name):
    # download_poster
    # is_movie_in_imdb = is_movie_exist_in_tmdb(movie_name)
    # print(f"is_movie in imdb: {is_movie_in_imdb}")

    if True:
        tmdb = TMDBDownloader(movie_name)
        filename = tmdb.download_poster_file()
        print(f"Movie {tmdb.movie_name} poster was downloaded from TMDB web API to the posters directory")
        # mongo_db.write_image_file(tmdb.movie_name, poster_path, tmdb.imdb_id)
    else:
        print(f"The movie '{movie_name}' was not found in IMDB also.")
    # todo
    # run the code from app server see if get_poster_from_tmdb_website works

def get_poster_from_mongo_db(movie_name, mongo_db):
    mongo_db.download_file_from_db()
    print(f"Movie {movie_name} poster was downloaded from MongoDB to the posters directory")


def download_poster_to_user_pc(movie_name):
    """Gets a movie name and download the poster to the user's PC"""
    ip = "127.0.0.1"
    port = 27017
    is_poster_in_mongo = is_file_exist_in_mongo(movie_name, ip, port)
    if is_poster_in_mongo:
        print(f"going to download from MongoDB")
        mongo_db = MongoDB("127.0.0.1", 27017, movie_name)
        get_poster_from_mongo_db(movie_name, mongo_db)

    else:
        print(f"going to download from TMDB")
        get_poster_from_tmdb_website(movie_name)
