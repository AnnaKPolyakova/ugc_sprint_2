import random
import uuid
from datetime import datetime

from research.settings_for_testing import (
    OBJECT_COUNTS_INSERT_IN_ONE_TIME,
    PROBABILITIES,
    USER_IDS,
)


def get_bookmark_list_of_dict(number=OBJECT_COUNTS_INSERT_IN_ONE_TIME):
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
            {
                'id': uuid.uuid4(),
                'create_at': datetime.utcnow(),
                'user_id': user_id,
                'movie_id': uuid.uuid4(),
            },
        )
    return bookmark_list_objs


def get_movie_ratings_list_of_dict(number=OBJECT_COUNTS_INSERT_IN_ONE_TIME):
    """
    Generate a list of movie rating with this function.

    Args:
        number (int): The number of dictionaries to generate.

    Returns:
        A list of generated dictionaries.
    """
    movie_ratings_objs = []
    for _ in range(0, number):
        user_id = random.choices(USER_IDS, PROBABILITIES)[0]
        movie_ratings_objs.append(
            {
                'id': uuid.uuid4(),
                'create_at': datetime.utcnow(),
                'user_id': user_id,
                'movie_id': uuid.uuid4(),
                'rating': random.choices([1, 10])[0],
            },
        )
    return movie_ratings_objs
