import subprocess

from pymongo import MongoClient

from users_actions_app.settings import app_settings

mongodb_client: MongoClient = MongoClient(
    app_settings.mongo_host, app_settings.mongo_port
)


def mongodb_init(client, settings):
    subprocess.call(["sh", "../mongo/entrypoint.sh"])
    admin = client.admin
    db = client[settings.db_name]
    admin.command("enableSharding", settings.db_name)
    for name in [
        settings.review_rating_collection,
        settings.movie_review_collection,
        settings.movie_rating_collection,
        settings.bookmark_collection,
    ]:
        collection = db[name]
        admin.command(
            {
                "shardCollection": collection.full_name,
                "key": {"user_id": "hashed"}
            }
        )
    return client[settings.db_name]
