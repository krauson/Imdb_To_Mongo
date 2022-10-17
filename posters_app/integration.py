from tmbd_downloader import TMDBDownloader
from mongo_funcs import MongoDB, is_file_exist_in_mongo


def get_poster_from_tmdb_website(movie_name):

    tmdb = TMDBDownloader(movie_name)

    tmdb.download_poster_file()
    print(f"Movie {tmdb.movie_name} poster was downloaded successfully from TMDB web API to the posters directory")
    return tmdb.poster_url

def get_poster_from_mongo_db(movie_name, mongo_db):
    poster_url = mongo_db.download_poster_from_db()
    print(f"Movie {movie_name} poster was downloaded from MongoDB to the posters directory")
    return poster_url

def download_poster_to_user_pc(movie_name):
    """Gets a movie name and download the poster to the user's PC"""
    host = "db-movie"
    port = 27017
    is_poster_in_mongo = is_file_exist_in_mongo(movie_name, host, port)
    mongo_db = MongoDB(host, port, movie_name)

    if is_poster_in_mongo:
        print(f"Trying to download from MongoDB..")
        mongo_db.set_file_metadata()
        mongo_db.set_file_id()
        get_poster_from_mongo_db(movie_name, mongo_db)
        mongo_db.set_file_metadata()
        poster_url = mongo_db.file_metadata['poster_url']


    else:
        print(f"Trying to download from TMDB..")
        poster_url = get_poster_from_tmdb_website(movie_name)
        # insert_poster_to_mongoDB
        mongo_db.write_to_mongo(poster_url)

    return poster_url

