from datetime import datetime

import mongoengine as me

from tests.functional.settings import test_settings


class MovieRatingMongo(me.Document):
    create_at = me.DateTimeField(default=datetime.now, auto_now_add=True)
    movie_id = me.StringField()
    user_id = me.StringField()
    rating = me.IntField()

    meta = {"collection": test_settings.movie_rating_collection}


class MovieReviewMongo(me.Document):
    create_at = me.DateTimeField(default=datetime.now, auto_now_add=True)
    text = me.StringField()
    movie_id = me.StringField()
    user_id = me.StringField()
    rating_id = me.ObjectIdField()

    meta = {"collection": test_settings.movie_review_collection}


class ReviewRatingMongo(me.Document):
    create_at = me.DateTimeField(default=datetime.now, auto_now_add=True)
    movie_id = me.StringField()
    user_id = me.StringField()
    review_id = me.ObjectIdField()
    rating = me.IntField()

    meta = {"collection": test_settings.review_rating_collection}


class BookmarkMongo(me.Document):
    create_at = me.DateTimeField(default=datetime.now, auto_now_add=True)
    movie_id = me.StringField()
    user_id = me.StringField()

    meta = {"collection": test_settings.bookmark_collection}
