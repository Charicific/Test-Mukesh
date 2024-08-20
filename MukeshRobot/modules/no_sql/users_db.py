from MukeshRobot import MONGO_DB_URI
from pymongo import MongoClient
from MukeshRobot.modules.no_sql import get_collection

myclient = MongoClient(MONGO_DB_URI)

users =myclient["MUK_users"]
usersdb = users["MUK_users"]

ban_db=users["gban_db"]

USERS_DB = get_collection("USERS")
CHATS_DB = get_collection("CHATS")
CHAT_MEMBERS_DB = get_collection("CHAT_MEMBERS")


def ensure_bot_in_db():
    USERS_DB.update_one(
        {"_id": dispatcher.bot.id},
        {"$set": {"username": dispatcher.bot.username}},
        upsert=True,
    )


def update_user(user_id, username, chat_id=None, chat_name=None):
    USERS_DB.update_one({"_id": user_id}, {"$set": {"username": username}}, upsert=True)

    if not (chat_id or chat_name):
        return

    CHATS_DB.update_one(
        {"chat_id": chat_id}, {"$set": {"chat_name": chat_name}}, upsert=True
    )

    member = CHAT_MEMBERS_DB.find_one({"chat_id": chat_id, "user_id": user_id})
    if member is None:
        CHAT_MEMBERS_DB.insert_one({"chat_id": chat_id, "user_id": user_id})


def get_userid_by_name(username) -> dict:
    return list(USERS_DB.find({"username": username}))


def is_served_user(user_id: int) -> bool:
    user = usersdb.find_one({"user_id": user_id})
    if user is not None:  # Check if the user is not None before using await
        return True
    return False

def get_served_users() -> list:
    users_list = []
    for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list

def save_id(user_id: int):
    is_served = is_served_user(user_id)
    if is_served:
        return
    usersdb.insert_one({"user_id": user_id})

def remove_served_users(user_id: int):
    is_served = is_served_user(user_id)
    if not is_served:
        return
    usersdb.delete_one({"user_id": user_id})
    
    
