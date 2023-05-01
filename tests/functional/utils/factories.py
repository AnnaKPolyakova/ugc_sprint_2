import random
import uuid

import factory
import mongoengine as me

from tests.functional.settings import test_settings
from tests.functional.utils.models import (
    BookmarkMongo,
    MovieRatingMongo,
    MovieReviewMongo,
    ReviewRatingMongo,
)
from users_actions_app.init_db import mongodb_client

db = mongodb_client[test_settings.db_name]

me.connect(
    db=test_settings.db_name,
    host=test_settings.mongo_host,
    port=test_settings.mongo_port,
)


class MovieRatingFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = MovieRatingMongo

    movie_id = factory.LazyAttribute(lambda a: str(uuid.uuid4()))
    user_id = factory.LazyAttribute(lambda a: str(uuid.uuid4()))
    rating = factory.LazyAttribute(lambda a: random.choice([1, 10]))


class MovieReviewFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = MovieReviewMongo

    text = factory.Faker("sentence", locale="en_US", nb_words=5)
    movie_id = factory.LazyAttribute(lambda a: str(uuid.uuid4()))
    user_id = factory.LazyAttribute(lambda a: str(uuid.uuid4()))
    rating_id = factory.LazyAttribute(lambda a: MovieRatingFactory().id)


class ReviewRatingFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = ReviewRatingMongo

    user_id = factory.LazyAttribute(lambda a: str(uuid.uuid4()))
    review_id = factory.LazyAttribute(lambda a: MovieReviewFactory().id)
    rating = factory.LazyAttribute(lambda a: random.choice([1, 10]))


class BookmarkFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = BookmarkMongo

    user_id = factory.LazyAttribute(lambda a: str(uuid.uuid4()))
    movie_id = factory.LazyAttribute(lambda a: str(uuid.uuid4()))
