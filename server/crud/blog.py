import datetime

from typing import List, Optional
from pymongo.database import Database
from pymongo.collection import Collection
from bson import ObjectId

from schemas.blog import BlogCreate, Blog
from utils.func import convert_object_id_of_item

from core.logger import get_logger

logger = get_logger(__name__)


def get_blog_collection(db: Database) -> Collection:
  return db.get_collection("blogs")


def create_blog(db: Database, blog: BlogCreate) -> Blog:
  collection = get_blog_collection(db)
  blog_dict = blog.model_dump()

  del blog_dict['image']

  now = datetime.datetime.now()
  blog_dict["created_at"] = now
  blog_dict["updated_at"] = now

  result = collection.insert_one(blog_dict)

  created_blog_data = collection.find_one({"_id": result.inserted_id})
  if created_blog_data:
    created_blog_data = convert_object_id_of_item(created_blog_data)

  return Blog(**created_blog_data)


def delete_blog(db: Database, blog_id: str) -> bool:
  collection = get_blog_collection(db)
  result = collection.delete_one({"_id": ObjectId(blog_id)})
  return result.deleted_count > 0


def update_blog(db: Database, blog_id: str, blog: BlogCreate) -> Blog:
  collection = get_blog_collection(db)
  blog_dict = blog.model_dump()

  del blog_dict['image']

  now = datetime.datetime.now()
  blog_dict["updated_at"] = now

  result = collection.update_one({"_id": ObjectId(blog_id)}, {"$set": blog_dict})

  updated_blog_data = collection.find_one({"_id": ObjectId(blog_id)})
  if updated_blog_data:
    updated_blog_data = convert_object_id_of_item(updated_blog_data)

  return Blog(**updated_blog_data)


def get_blog(db: Database, blog_id: str) -> Optional[Blog]:
  collection = get_blog_collection(db)
  try:
    blog_data = collection.find_one({"_id": ObjectId(blog_id)})
    if blog_data:
      blog_data = convert_object_id_of_item(blog_data)
      return Blog(**blog_data)
    return None
  except Exception as e:
    print(f"Error fetching blog by id: {e}")
    return None


def get_blogs(db: Database, skip: int = 0, limit: int = 100) -> List[Blog]:
  collection = get_blog_collection(db)
  blogs_cursor = collection.find().skip(skip).limit(limit)

  result = []
  for blog_data in blogs_cursor:
    blog_data = convert_object_id_of_item(blog_data)
    result.append(Blog(**blog_data))

  return result
