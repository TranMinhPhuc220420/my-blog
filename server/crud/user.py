import datetime

from typing import List, Optional
from pymongo.database import Database
from pymongo.collection import Collection
from bson import ObjectId

from schemas.auth import UserCreate, User
from utils.func import convert_object_id_of_item, convert_username
from core.security import hash_password


def get_user_collection(db: Database) -> Collection:
  return db.get_collection("users")


def create_user(db: Database, username: str, password: str) -> User:
  collection = get_user_collection(db)

  now = datetime.datetime.now()
  user_dict = {
    "username": convert_username(username),
    "hashed_password": hash_password(password),
    "created_at": now,
    "updated_at": now
  }
  result = collection.insert_one(user_dict)

  created_user_data = collection.find_one({"_id": result.inserted_id})
  if created_user_data:
    created_user_data = convert_object_id_of_item(created_user_data)

  return User(**created_user_data)


def get_user(db: Database, user_id: str) -> Optional[User]:
  collection = get_user_collection(db)
  try:
    user_data = collection.find_one({"_id": ObjectId(user_id)})
    if user_data:
      user_data = convert_object_id_of_item(user_data)
      return User(**user_data)
    return None
  except Exception as e:
    print(f"Error fetching user by id: {e}")
    return None


def get_users(db: Database, skip: int = 0, limit: int = 100) -> List[User]:
  collection = get_user_collection(db)
  users_cursor = collection.find().skip(skip).limit(limit)

  result = []
  for user_data in users_cursor:
    user_data = convert_object_id_of_item(user_data)
    result.append(User(**user_data))

  return result


def get_user_by_username(db: Database, username: str):
  collection = get_user_collection(db)
  try:
    username = convert_username(username)
    user_data = collection.find_one({"username": username})
    if user_data:
      user_data = convert_object_id_of_item(user_data)
      return User(**user_data)
    return None
  except Exception as e:
    print(f"Error fetching user by username: {e}")
    return None


def set_refresh_token_for_user(db: Database, user_id: str, refresh_token: str):
  collection = get_user_collection(db)
  collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"refresh_token": refresh_token}})


def get_refresh_token_for_user(db: Database, user_id: str) -> Optional[str]:
  collection = get_user_collection(db)
  user_data = collection.find_one({"_id": ObjectId(user_id)})
  if user_data:
    return user_data.get("refresh_token")
  return None


def set_info_login(db: Database, user_id: str, device_info: dict):
  collection = get_user_collection(db)
  collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"device_info": device_info}})


def get_info_login(db: Database, user_id: str) -> Optional[dict]:
  collection = get_user_collection(db)
  user_data = collection.find_one({"_id": ObjectId(user_id)})
  if user_data:
    return user_data.get("device_info")
  return None


def remove_info_login(db: Database, user_id: str):
  collection = get_user_collection(db)
  collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"refresh_token": None, "device_info": None}})


def set_role_for_user(db: Database, user_id: str, role: str):
  collection = get_user_collection(db)
  collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"role": role}})
