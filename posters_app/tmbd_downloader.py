import requests
from config_file import API_KEY, content_path
import imdb
import os
import sys


def convert_image_size_to_int(x: str) -> int:
    """sorting function to get the biggest picture size """
    return float("inf") if x == 'original' else int(x[1:])


class TMDBDownloader:
    content_path = content_path

    def __init__(self, movie_name):
        self.IMAGE_CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'
        self.IMAGE_REQUEST_PATTERN = 'http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}'
        self.KEY = API_KEY
        self.url = self.IMAGE_CONFIG_PATTERN.format(key=self.KEY)
        self.config = requests.get(self.url).json()
        self.image_base_url = self.config['images']['base_url']
        self.sizes = self.config['images']['poster_sizes']
        # use the sort function in max to get biggest size
        self.max_size = max(self.sizes, key=convert_image_size_to_int)
        self.movie_name = movie_name         # check name for legality
        self.imdb_id = self.get_movie_id()
        self.filename = movie_name + '_poster.jpeg'
        self.poster_url = ""

    def get_movie_id(self):
        imdb_obj = imdb.IMDb()
        movies = imdb_obj.search_movie(self.movie_name)
        print(f"movies:{movies}")
        try:
            print(f"movies[0]:{movies[0]}")
            imdb_id = "tt" + str(movies[0].movieID)
            return imdb_id

        except IndexError as e:
            print(e)
            print("Refresh and try again in a minute, too frequent API requests")

    def get_poster_url(self):
        img_url_request = self.IMAGE_REQUEST_PATTERN.format(
            key=self.KEY, imdbid=self.imdb_id)
        api_response = requests.get(img_url_request).json()
        try:
            # print(f"api_response[posters]:{api_response['posters']}")
            posters = api_response['posters']
            poster_urls = []
            for poster in posters:
                rel_path = poster['file_path']
                url = "{0}{1}{2}".format(
                    self.image_base_url, self.max_size, rel_path)
                poster_urls.append(url)
            poster_url = poster_urls[0]
            self.poster_url = poster_url
            print(f"poster_url = {poster_url}")
            return poster_url  # return only the first poster url

        except KeyError:
            print(KeyError)
            return None

    def download_poster_file(self):
        poster_url = self.get_poster_url()
        poster_data = requests.get(poster_url)
        poster_binary = poster_data.content

        print(f"sys.platform:{sys.platform}")
        target_path = '/'.join([content_path, self.filename])
        # target_path = '\\'.join([content_path, self.filename])
        print(f"target_path: {target_path}")
        with open(target_path, 'wb') as image_file:
            image_file.write(poster_binary)
        print(f"{self.movie_name} was downloaded succussfully to {content_path}.")


def main():
    movie_name = "spiderman"
    tmbd_conn = TMDBDownloader(movie_name)
    print(tmbd_conn.download_poster_file())


if __name__ == '__main__':
    main()
