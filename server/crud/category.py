import datetime

from typing import List, Optional
from pymongo.database import Database
from pymongo.collection import Collection
from bson import ObjectId

from schemas.category import CategoryCreate, Category
from utils.func import convert_object_id_of_item

from core.logger import get_logger

logger = get_logger(__name__)

def get_category_collection(db: Database) -> Collection:
  return db.get_collection("categories")


def create_category(db: Database, category: CategoryCreate) -> Category:
  collection = get_category_collection(db)
  category_dict = category.model_dump()

  logger.info(category_dict)

  now = datetime.datetime.now()
  category_dict["created_at"] = now
  category_dict["updated_at"] = now

  result = collection.insert_one(category_dict)

  created_category_data = collection.find_one({"_id": result.inserted_id})
  if created_category_data:
    created_category_data = convert_object_id_of_item(created_category_data)

  return Category(**created_category_data)

def delete_category(db: Database, category_id: str) -> bool:
  collection = get_category_collection(db)
  result = collection.delete_one({"_id": ObjectId(category_id)})
  return result.deleted_count > 0

def update_category(db: Database, category_id: str, category: CategoryCreate) -> Category:
  collection = get_category_collection(db)
  category_dict = category.model_dump()

  now = datetime.datetime.now()
  category_dict["updated_at"] = now

  result = collection.update_one({"_id": ObjectId(category_id)}, {"$set": category_dict})

  updated_category_data = collection.find_one({"_id": ObjectId(category_id)})
  if updated_category_data:
    updated_category_data = convert_object_id_of_item(updated_category_data)

  return Category(**updated_category_data)

def get_category(db: Database, category_id: str) -> Optional[Category]:
  collection = get_category_collection(db)
  try:
    category_data = collection.find_one({"_id": ObjectId(category_id)})
    if category_data:
      category_data = convert_object_id_of_item(category_data)
      return Category(**category_data)
    return None
  except Exception as e:
    print(f"Error fetching category by id: {e}")
    return None


def get_categories(db: Database, skip: int = 0, limit: int = 100) -> List[Category]:
  collection = get_category_collection(db)
  categories_cursor = collection.find().skip(skip).limit(limit)

  result = []
  for category_data in categories_cursor:
    category_data = convert_object_id_of_item(category_data)
    result.append(Category(**category_data))

  return result
