from pymongo import MongoClient
import gridfs
from config_file import content_path


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
        self.file_metadata = None
        self.file_id = None

    def write_to_mongo(self, poster_url):
        """Writes an image file to the DB"""
        file_path = self.content_path + '\\' + self.filename
        with open(file_path, 'rb') as image_file:
            data_binary = image_file.read()
            self.fs.put(data_binary, filename=self.filename, poster_url=poster_url)
        print(f"Image {self.filename} was inserted to mongoDB")


    def set_file_id(self):
        file_id = self.file_metadata['_id']
        self.file_id = file_id

    def set_file_metadata(self):
        regex_query = {"filename": {"$regex": f"^{self.filename}"}}
        file_metadata = self.db.fs.files.find_one(regex_query)
        print(f"file_metadata: {file_metadata}")
        if file_metadata is None:
            print("file was not found.")
            return False
        else:
            self.file_metadata = file_metadata
            return True


    # def read_image_file(self):
    #     output_data = self.fs.get(self.file_id).read()
    #     # print(f"output_data: {output_data}")
    #     # print(output_data)
    #     return output_data

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

    def download_poster_from_db(self):
        print(f"in download download_file_from_mongodb . filename = {self.filename}")
        poster_bytes = self.fs.get(self.file_id).read()
        print(f"data in bytes: {poster_bytes[:10]}")

        target_path = self.content_path + '\\' + self.filename
        print(f"target_path = {target_path}")
        with open(target_path, 'wb') as output_file:
            output_file.write(poster_bytes)


if __name__ == "__main__":
    """
    test module
    """
    mdb = MongoDB("localhost", 27017, "venom")
    # mdb.download_file_from_db()

    poster_abs_path = r"C:\Users\Hagai\Desktop\AWS\course projects\Imdb_To_Mongo\posters\matrix_poster.jpeg"

    mdb.write_to_mongo(poster_abs_path, "1")

