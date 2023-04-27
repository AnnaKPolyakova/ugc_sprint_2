import logging
import subprocess

from clickhouse_driver import Client

from research.clickhouse.data_lists_generators import (
    OBJECT_COUNTS_INSERT_IN_ONE_TIME,
    get_bookmark_list,
    get_movie_ratings_list,
)
from research.settings_for_testing import USER_ID
from research.utils import dictConfig  # noqa: F401
from research.utils import measure_time

START_NAME = "start {name}"


class ClickhouseTest:
    def __init__(self, clear_db=False, insert_obj_in_db=0):
        self.clear_db = clear_db
        self.insert_obj_in_db = insert_obj_in_db
        self.client = Client(host="localhost")

    def _init_test_db(self):
        logging.info(START_NAME.format(name=self._init_test_db.__name__))
        subprocess.call(["sh", "entrypoint.sh"])

    def _clear_db(self):
        logging.info(START_NAME.format(name=self._clear_db.__name__))
        self.client.execute("TRUNCATE TABLE default.bookmark_test")
        self.client.execute("TRUNCATE TABLE default.movie_rating_test")

    def _add_obj_in_db(self):
        logging.info(START_NAME.format(name=self._add_obj_in_db.__name__))
        counts = self.insert_obj_in_db // OBJECT_COUNTS_INSERT_IN_ONE_TIME
        for iteration in range(0, counts):
            logging.info(
                "insert {i} time from {counts}".format(
                    i=iteration, counts=counts
                )
            )
            try:
                bookmark_objs = get_bookmark_list()
                self.client.execute(
                    "INSERT INTO default.bookmark_test ("
                    "id, create_at, user_id, movie_id"
                    ") VALUES",
                    bookmark_objs,
                )
                movie_ratings_objs = get_movie_ratings_list()
                self.client.execute(
                    "INSERT INTO default.movie_rating_test ("
                    "id, create_at, user_id, movie_id, rating"
                    ") VALUES",
                    movie_ratings_objs,
                )
            except Exception as error:
                logging.error(error)

    def _count_obj(self):
        logging.info(START_NAME.format(name=self._count_obj.__name__))
        result_rating = self.client.execute(
            "SELECT COUNT(id) FROM default.movie_rating_test"
        )[0][0]
        result_bookmark = self.client.execute(
            "SELECT COUNT(id) FROM default.bookmark_test"
        )[0][0]
        with open("result.txt", "a") as result_file:
            result_file.write(
                '{result_rating}\n{result_bookmark}\n'.format(
                    result_rating=str(result_rating),
                    result_bookmark=str(result_bookmark),
                )
            )

    @measure_time
    def _get_users_favorite_movies_from_full_db(self):
        self.client.execute(
            "SELECT * FROM default.movie_rating_test "
            "WHERE user_id = {user_id} AND rating = 1".format(user_id=USER_ID)
        )

    @measure_time
    def _get_users_bookmark_from_full_db(self):
        self.client.execute(
            "SELECT * FROM default.bookmark_test "
            "WHERE user_id = {user_id}".format(user_id=USER_ID)
        )

    def run_tests(self):
        self._init_test_db()
        if self.clear_db:
            self._clear_db()
        if self.insert_obj_in_db > 0:
            self._add_obj_in_db()
        self._count_obj()
        self._get_users_favorite_movies_from_full_db()
        self._get_users_bookmark_from_full_db()


if __name__ == "__main__":
    tests = ClickhouseTest()
    tests.run_tests()
