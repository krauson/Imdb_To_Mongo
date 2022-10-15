from tmbd_download_image import TMDBDownloader
from mongo_funcs import MongoDB, is_file_exist_in_mongo


def get_poster_from_tmdb_website(movie_name):

    tmdb = TMDBDownloader(movie_name)

    answer = tmdb.download_poster_file()
    print(f"answer:{answer}")
    print(f"Movie {tmdb.movie_name} poster was downloaded succussfully from TMDB web API to the posters directory")


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

    # if tmdb.movie_data is None:
    #     print(f"""
    #     Couldn't download the poster, two possible reasons:
    #     1.The movie '{movie_name}' was not found in IMDB.
    #     2.There API requests to IMDB were too frequent.
    #     """)
    # else: