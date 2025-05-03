# Standard libraries
from typing import List, Annotated

from bson import Binary
# FastAPI libraries
from fastapi import APIRouter, Depends, HTTPException
from fastapi import Request, Response, status
from starlette.responses import StreamingResponse, FileResponse, Response

# MongoDB
from pymongo.database import Database

from db.mongodb import get_mongo_db, set_namespace
from services.auth_service import check_login

# Utils
from utils import func

# Core
from core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/{namespace}/images/blogs/{filename}", status_code=status.HTTP_200_OK)
def get_image_blog(
    namespace: str,
    filename: str,
    w: int = None,
    h: int = None
):
  """
  Get the image of a blog
  Args:
      filename (str): Name of the file
      namespace (str): The namespace to set for the database.
      w (int): The width of the image
      h (int): The height of the image
  Returns:
      FileResponse: The image
  """

  storage_dir = func.get_root_path_project() / "storage" / namespace / 'blogs'
  file_path = storage_dir / filename

  # Check if file exists
  if not file_path.exists():
    raise HTTPException(status_code=404, detail="File not found")

  # Set headers for cache for 5 minutes
  response = Response()
  response.headers['Cache-Control'] = 'max-age=300'

  if w or h:
    width = w
    height = h

    if not width and height:
      width = height
    if not height and width:
      height = width

    image_io_resized, format_save = func.resize_image(file_path, width, height)

    # Content length
    response.headers['Content-Length'] = str(len(image_io_resized.getvalue()))

    return StreamingResponse(image_io_resized, headers=response.headers, media_type=f"image/{format_save.lower()}")

  return FileResponse(file_path)
