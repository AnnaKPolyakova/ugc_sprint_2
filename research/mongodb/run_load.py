import logging
import subprocess
from time import sleep

from pymongo import MongoClient

from research.mongodb.data_lists_generators import (
    get_bookmark_list_of_dict,
    get_movie_ratings_list_of_dict,
)
from research.settings_for_testing import (
    NUMBER_OF_OBJECTS_TO_LOAD_BY_INSERTION
)
from research.utils import dictConfig  # noqa: F401


class MongodbLoad:
    def __init__(self):
        self.client = MongoClient(
            "mongodb://localhost:27019/?uuidRepresentation=standard"
        )
        self.bookmark_test_collection = None
        self.movie_rating_test_collection = None

    def _init_test_db(self):
        subprocess.call(["sh", "entrypoint.sh"])
        admin = self.client.admin
        db = self.client["test"]
        admin.command("enableSharding", "test")
        self.bookmark_test_collection = db["bookmark_test"]
        admin.command(
            {
                "shardCollection": self.bookmark_test_collection.full_name,
                "key": {"create_at": "hashed"},
            }
        )
        self.movie_rating_test_collection = db["movie_rating_test"]
        admin.command(
            {
                "shardCollection": self.movie_rating_test_collection.full_name,
                "key": {"create_at": "hashed"},
            }
        )

    def _insert(self):
        count = 0
        while True:
            sleep(0.1)
            bookmark_objs = get_bookmark_list_of_dict(
                number=NUMBER_OF_OBJECTS_TO_LOAD_BY_INSERTION
            )
            movie_rating_objs = get_movie_ratings_list_of_dict(
                number=NUMBER_OF_OBJECTS_TO_LOAD_BY_INSERTION
            )
            try:
                self.bookmark_test_collection.insert_many(bookmark_objs)
                self.movie_rating_test_collection.insert_many(
                    movie_rating_objs
                )
            except Exception as error:
                logging.info(error)
            else:
                count += 1
                logging.info(count)

    def run(self):
        with open("result.txt", "a") as result_file:
            result_file.write("Нагрузка\n")
        self._init_test_db()
        self._insert()


if __name__ == "__main__":
    load = MongodbLoad()
    load.run()
