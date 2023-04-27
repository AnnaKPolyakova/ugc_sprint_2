import random
import uuid
from datetime import datetime

from research.settings_for_testing import (
    OBJECT_COUNTS_INSERT_IN_ONE_TIME,
    PROBABILITIES,
    USER_IDS,
)


def get_bookmark_list(number=OBJECT_COUNTS_INSERT_IN_ONE_TIME):
    """
    Generate a list of bookmark with this function.

    Args:
        number (int): The number of dictionaries to generate.

    Returns:
        A list of generated dictionaries.
    """
    bookmark_list_objs = []
    for _ in range(0, number):
        user_id = random.choices(USER_IDS, PROBABILITIES)[0]
        bookmark_list_objs.append(
            (uuid.uuid4(), datetime.utcnow(), user_id, uuid.uuid4())
        )
    return bookmark_list_objs


def get_movie_ratings_list(number=OBJECT_COUNTS_INSERT_IN_ONE_TIME):
    """
    Generate a list of movie rating with this function.

    Args:
        number (int): The number of dictionaries to generate.

    Returns:
        A list of generated dictionaries.
    """
    movie_rating_objs = []
    for _ in range(0, number):
        user_id = random.choices(USER_IDS, PROBABILITIES)[0]
        movie_rating_objs.append(
            (
                uuid.uuid4(),
                datetime.utcnow(),
                user_id,
                uuid.uuid4(),
                random.choices([1, 10])[0],
            )
        )
    return movie_rating_objs
