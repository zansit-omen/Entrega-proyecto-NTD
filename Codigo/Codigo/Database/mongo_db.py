import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
MONGO_DB_NAME = os.getenv("MONGODB_DB", "chats_db")
MONGO_CHAT_COLLECTION = os.getenv("MONGODB_CHAT_COLLECTION", "chats")

cliente = None
DbNoSQL = None


def get_mongo_client():
    global cliente

    if cliente is None:
        if not MONGO_URI:
            raise RuntimeError("No se encontro la variable MONGODB_URI")

        cliente = MongoClient(
            MONGO_URI,
            connect=False,
            serverSelectionTimeoutMS=5000,
        )

    return cliente


def get_mongo_db():
    global DbNoSQL

    if DbNoSQL is None:
        DbNoSQL = get_mongo_client()[MONGO_DB_NAME]

    return DbNoSQL


def get_chats_collection():
    return get_mongo_db()[MONGO_CHAT_COLLECTION]


class LazyCollection:
    def __getattr__(self, name):
        return getattr(get_chats_collection(), name)


chats = LazyCollection()
