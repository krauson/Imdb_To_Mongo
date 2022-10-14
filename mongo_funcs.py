from pymongo import MongoClient
import gridfs
import logging
from config_file import content_path

logging.basicConfig(level=logging.DEBUG)


class MongoDB:
    content_path = content_path

    def __init__(self, ip, port, movie_name):
        # connect to DB:
        db = MongoClient(ip, port).posters
        fs = gridfs.GridFS(db)
        self.fs = fs
        self.db = db
        self.movie_name = movie_name
        self.filename_prefix = movie_name + "_poster"


    def write_image_file(self, file_path, imdb_code):
        """Writes an image file to the DB"""

        with open(file_path, 'rb') as image_file:
            data = image_file.read()
            filename = file_path.split('\\')[-1]
            self.fs.put(data, filename=filename, imdb_code=imdb_code)
        print(f"Image {filename} was inserted to mongoDB")

    def get_file_id(self):
        regex_query = {"filename": {"$regex": f"^{self.filename_prefix}"}}
        is_file_exist = False
        reg_mydoc = self.fs.find(regex_query)
        file_metadata = self.db.fs.files.find_one(regex_query)
        print(f"file_metadata {file_metadata}")
        if file_metadata is None:
            response = False
        else:
            logging.debug(f"file id for the movie {movie_name}: {file_metadata['_id']}")
            response = file_metadata['_id']
        return response

    def read_image_file(self):
        file_id = self.get_file_id(self.movie_name)
        output_data = self.fs.get(file_id).read()
        print(f"output_data: {output_data}")
        return output_data

    def del_image_file(self,movie_name):
        file_id = self.get_file_id(movie_name)
        self.fs.delete(file_id)
        print(f"File {movie_name} was deleted from DB.")

    def update_image_file_meta_data(self, movie_name, key_to_update, val_to_update):
        file_id = self.get_file_id(movie_name)
        new_query = {key_to_update: val_to_update}
        # self.db.fs.files.update({'_id': file_id}, {'$set': new_query})
        files_collection = self.db["fs.files"]
        filter_query = {'_id': file_id}
        db_update_response = files_collection.update_one(filter_query, {"$set": new_query})
        output = {'Status': 'Successfully Updated' if db_update_response.modified_count > 0 else "Nothing was updated."}
        return output


    def is_filename_exist(self):
        print(f"prefix_filename = {self.filename_prefix}")
        regex_query = {"filename": {"$regex": f"^{self.filename_prefix}"}}
        is_file_exist = False
        reg_mydoc = self.fs.find(regex_query)

        for _ in reg_mydoc: # if the loop will go at least one time the regex exp exists
            print(f"file {self.filename_prefix} was found in MongoDB")
            is_file_exist = True

        if not is_file_exist:
            print(f"file {self.filename_prefix} was not found in MongoDB")
        return is_file_exist


    def get_full_filename(self):
        print("in get full filename")
        regex_query = {"filename": {"$regex": f"^{self.filename_prefix}"}}
        reg_mydoc = self.fs.find(regex_query)
        for doc in reg_mydoc: # if the loop will go at least one time the regex exp exists
            print(f"doc: {doc}")
            for i in doc:
                print(i)

    def download_file_from_db(self):
        print(f"in download from mongo. filename = {self.filename_prefix}")
        file_id = self.get_file_id()
        print(f"file_id = {file_id}")
        poster_bytes = self.fs.get(file_id).read()
        print(f"output_data: {poster_bytes}")

        target_path = target_location + '\\' + filename
        print(f"target_path = {target_path}")
        with open(target_path, 'wb') as output_file:
            output_file.write(poster_bytes)
        print(f"File {filename} was dowloaded to: {target_path}")


if __name__ == "__main__":
    """
    test module
    """
    mdb = MongoDB("localhost", 27017, "Frozen")
    mdb.download_file_from_db()



    # mdb.write_image_file(poster_abs_path, "bla-bla")
    print(mdb.is_filename_exist())
    # mdb.get_full_filename()
    # mdb.is_file_exist(movie_name)
    # mdb.read_image_file()
    # print(mdb.update_image_file_meta_data(movie_name, "filename2", "updated"))
    # mdb.del_image_file("spiderman")

    # filename = "Frozen_poster.jpeg"
    # poster_abs_path = r"C:\Users\Hagai\Desktop\AWS\course projects\Imdb_To_Mongo\posters\Frozen_poster.jpeg"
    # target_path = '\\'.join(target_path)
    # print(target_path)
    # target_path = poster_abs_path.split('\\')[:-1]


