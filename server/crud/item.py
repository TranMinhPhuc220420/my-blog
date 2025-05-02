import datetime

from typing import List, Optional
from pymongo.database import Database
from pymongo.collection import Collection
from bson import ObjectId

from schemas.item import ItemCreate, Item
from utils.func import convert_object_id_to_str

def get_item_collection(db: Database) -> Collection:
    return db.get_collection("items")

def create_item(db: Database, item: ItemCreate) -> Item:
    collection = get_item_collection(db)
    item_dict = item.model_dump()

    now = datetime.datetime.now()
    item_dict["created_at"] = now
    item_dict["updated_at"] = now

    result = collection.insert_one(item_dict)

    created_item_data = collection.find_one({"_id": result.inserted_id})
    created_item_data['_id'] = convert_object_id_to_str(created_item_data['_id'])

    return Item(**created_item_data)

def get_item(db: Database, item_id: str) -> Optional[Item]:
    collection = get_item_collection(db)
    try:
        item_data = collection.find_one({"_id": ObjectId(item_id)})
        if item_data:
            item_data['_id'] = convert_object_id_to_str(item_data['_id'])
            return Item(**item_data)
        return None
    except Exception as e:
        print(f"Error fetching item by id: {e}")
        return None

def get_items(db: Database, skip: int = 0, limit: int = 100) -> List[Item]:
    collection = get_item_collection(db)
    items_cursor = collection.find().skip(skip).limit(limit)
    
    result = []
    for item_data in items_cursor:
        item_data['_id'] = convert_object_id_to_str(item_data['_id'])
        result.append(Item(**item_data))
    
    return result