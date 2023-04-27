from pymongo import MongoClient

from users_actions_app.settings import app_settings

mongodb_client: MongoClient = MongoClient(
    app_settings.mongo_host, app_settings.mongo_port
)


def mongodb_init(client):
    db = client[app_settings.db_name]
    admin = client.admin
    collection = db[app_settings.movie_rating_collection]
    admin.command("enableSharding", app_settings.db_name)
    admin.command(
        {"shardCollection": collection.full_name, "key": {"user_id": "hashed"}}
    )
    return client
