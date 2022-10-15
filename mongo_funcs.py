from pymongo import MongoClient
import gridfs
# import logging
from config_file import content_path

# logging.basicConfig(level=logging.DEBUG)

def format_filename(movie_name):
    return movie_name + '_poster.jpeg'


def is_file_exist_in_mongo(movie_name, ip, port):
    db = MongoClient(ip, port).posters
    fs = gridfs.GridFS(db)
    filename = format_filename(movie_name)
    regex_query = {"filename": {"$regex": f"^{filename}"}}
    is_file_exist = False
    reg_mydoc = fs.find(regex_query)

    for _ in reg_mydoc:  # if the loop will go at least one time the regex exp exists
        print(f"file {filename} was found in MongoDB")
        is_file_exist = True

    if not is_file_exist:
        print(f"file {filename} was not found in MongoDB")
    return is_file_exist


class MongoDB:
    content_path = content_path

    def __init__(self, ip, port, movie_name):
        # connect to DB:
        db = MongoClient(ip, port).posters
        fs = gridfs.GridFS(db)
        self.fs = fs
        self.db = db
        self.movie_name = movie_name
        self.filename = format_filename(movie_name)
        self.file_metadata = self.get_file_metadata()
        self.file_id = self.file_metadata['_id']


    def write_image_file(self, file_path, imdb_code):
        """Writes an image file to the DB"""

        with open(file_path, 'rb') as image_file:
            data = image_file.read()
            filename = file_path.split('\\')[-1]
            self.fs.put(data, filename=filename, imdb_code=imdb_code)
        print(f"Image {filename} was inserted to mongoDB")

    def get_file_metadata(self):
        regex_query = {"filename": {"$regex": f"^{self.filename}"}}
        file_metadata = self.db.fs.files.find_one(regex_query)
        print(f"file_metadata {file_metadata}")
        if file_metadata is None:
            print("file was not found.")
            return False
        else:
            # logging.debug(f"file id for the movie {self.movie_name}: {file_metadata['_id']}")
            # file_id = file_metadata['_id']
            return file_metadata

    def read_image_file(self):
        output_data = self.fs.get(self.file_id).read()
        # print(f"output_data: {output_data}")
        return output_data

    def del_image_file(self,movie_name):
        self.fs.delete(self.file_id)
        print(f"File {movie_name} was deleted from DB.")

    def update_image_file_meta_data(self, movie_name, key_to_update, val_to_update):
        new_query = {key_to_update: val_to_update}
        # self.db.fs.files.update({'_id': file_id}, {'$set': new_query})
        files_collection = self.db["fs.files"]
        filter_query = {'_id': self.file_id}
        db_update_response = files_collection.update_one(filter_query, {"$set": new_query})
        output = {'Status': 'Successfully Updated' if db_update_response.modified_count > 0 else "Nothing was updated."}
        return output


    def get_full_filename(self):
        print("in get full filename")
        regex_query = {"filename": {"$regex": f"^{self.filename}"}}
        reg_mydoc = self.fs.find(regex_query)
        for doc in reg_mydoc: # if the loop will go at least one time the regex exp exists
            print(f"doc: {doc}")
            for i in doc:
                print(i)

    def download_file_from_db(self):
        print(f"in download from mongo. filename = {self.filename}")
        poster_bytes = self.fs.get(self.file_id).read()
        print(f"output_data: {poster_bytes[:10]}")

        target_path = self.content_path + '\\' + self.filename
        print(f"target_path = {target_path}")
        with open(target_path, 'wb') as output_file:
            output_file.write(poster_bytes)
        print(f"File {self.filename} was dowloaded to: {target_path}")


if __name__ == "__main__":
    """
    test module
    """
    mdb = MongoDB("localhost", 27017, "Frozen")
    # mdb.download_file_from_db()



    # mdb.write_image_file(poster_abs_path, "bla-bla")
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


