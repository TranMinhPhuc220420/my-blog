from typing import Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId

def convert_objectid_to_str(obj: Any) -> str:
    if isinstance(obj, ObjectId):
        return str(obj)
    # Handle other types if necessary, though for this case ObjectId is main concern
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_offered: Optional[bool] = False

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: str = Field(alias="_id")
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        populate_by_name = True