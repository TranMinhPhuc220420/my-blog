from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime


class BlogBase(BaseModel):
  image_url: str
  title: str
  content: str
  author: str
  category: str
  tags: list
  comments: Optional[list] = []

class BlogCreate(BlogBase):
  pass


class Blog(BlogBase):
  id: str = Field(alias="_id")
  created_at: datetime = None
  updated_at: datetime = None

  class Config:
    populate_by_name = True
