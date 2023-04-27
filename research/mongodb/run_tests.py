import logging
import subprocess

from pymongo import MongoClient

from research.mongodb.data_lists_generators import (
    get_bookmark_list_of_dict,
    get_movie_ratings_list_of_dict,
)
from research.settings_for_testing import (
    OBJECT_COUNTS_INSERT_IN_ONE_TIME,
    USER_ID, TESTS_COUNT,
)
from research.utils import measure_time


class MongodbTest:
    def __init__(self, clear_db=False, insert_obj_in_db=0):
        self.clear_db = clear_db
        self.insert_obj_in_db = insert_obj_in_db
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

    def _clear_db(self):
        self.movie_rating_test_collection.delete_many({})
        self.bookmark_test_collection.delete_many({})

    def _add_obj_in_db(self):
        counts = self.insert_obj_in_db // OBJECT_COUNTS_INSERT_IN_ONE_TIME
        for iteration in range(0, counts):
            logging.info(
                'insert {i} time from {counts}'.format(
                    i=iteration,
                    counts=counts,
                )
            )
            bookmark_objs = get_bookmark_list_of_dict()
            movie_rating_objs = get_movie_ratings_list_of_dict()
            try:
                self.bookmark_test_collection.insert_many(bookmark_objs)
                self.movie_rating_test_collection.insert_many(
                    movie_rating_objs
                )
            except Exception as error:
                logging.error(error)

    @measure_time
    def _get_users_favorite_movies_from_full_db(self):
        for _ in range(TESTS_COUNT):
            self.movie_rating_test_collection.find(
                {'user_id': USER_ID, 'rating': 10}
            )

    def _count_obj(self):
        logging.info('start {name}'.format(name=self._count_obj.__name__))
        result_rating = self.movie_rating_test_collection.count_documents({})
        result_bookmark = self.bookmark_test_collection.count_documents({})
        with open('result.txt', 'a') as result_file:
            result_file.write(
                '{result_rating}\n{result_bookmark}\n'.format(
                    result_rating=str(result_rating),
                    result_bookmark=str(result_bookmark),
                )
            )

    @measure_time
    def _get_users_bookmark_from_full_db(self):
        for _ in range(TESTS_COUNT):
            self.bookmark_test_collection.find({'user_id': USER_ID})

    def run_tests(self):
        self._init_test_db()
        if self.clear_db:
            self._clear_db()
        if self.insert_obj_in_db > 0:
            self._add_obj_in_db()
        self._count_obj()
        self._get_users_favorite_movies_from_full_db()
        self._get_users_bookmark_from_full_db()


if __name__ == '__main__':
    tests = MongodbTest()
    tests.run_tests()
