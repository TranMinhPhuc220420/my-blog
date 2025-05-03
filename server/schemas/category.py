from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class CategoryBase(BaseModel):
  name: str
  color: str

class CategoryCreate(CategoryBase):
  pass


class Category(CategoryBase):
  id: str = Field(alias="_id")
  created_at: datetime = None
  updated_at: datetime = None

  class Config:
    populate_by_name = True
