from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, Field
from datetime import datetime


class BlogBase(BaseModel):
  title: str
  content: str
  author: str
  category: str
  tags: list
  image_url: Optional[str] = ''
  comments: Optional[list] = []

class BlogCreate(BlogBase):
  image: UploadFile


class Blog(BlogBase):
  id: str = Field(alias="_id")
  created_at: datetime = None
  updated_at: datetime = None

  class Config:
    populate_by_name = True
