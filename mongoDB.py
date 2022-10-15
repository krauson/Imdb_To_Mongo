from mongo_funcs import MongoDB
from pymongo import MongoClient
import gridfs

if __name__ == "__main__":
    """
    test module
    """

    mdb = MongoDB("localhost", 27017, "Frozen")
    files_collection = mdb.db["fs.files"]

    mdb.read_image_file()

    print(files_collection)

    filter_query = {'filename': "Frozen_poster.jpeg"}
    # db_update_response = files_collection.

    # for i in files_collection:
    #     print(i)


    # regex_query = {"filename": {"$regex": "^Frozen"}}
    # myquery = {"filename":  "Frozen_poster.jpeg"}
    # a = mdb.fs.put(b"hello world", filename="hagai")
    # print(a)
    # print(mdb.fs.get(a).read())

    # out = mdb.fs.find(myquery)
    # print(out)
    # out['filename']
    #
    # for i in out:
    #     print(dir(i))
    #     print(i['filename'])

    # mydb = mdb.db["posters"]
    #
    # file_colec = mydb["files"]
    # print(f"file_colec: {file_colec}")
    #
    # myquery = {"filename": {"$regex": "^Frozen"}}
    #
    # mydoc = file_colec.find(myquery)
    #
    # for x in mydoc:
    #     print(x)