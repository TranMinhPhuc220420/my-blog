from typing import Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


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
