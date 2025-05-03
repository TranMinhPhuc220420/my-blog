# Standard libraries
from typing import List, Annotated

# FastAPI libraries
from fastapi import APIRouter, Depends, HTTPException
from fastapi import Request, Response, status
from fastapi import Form

# MongoDB
from pymongo.database import Database
from starlette.responses import JSONResponse

from db.mongodb import get_mongo_db, set_namespace
from schemas.blog import BlogCreate, Blog
from crud import blog as crud_blog
from services.auth_service import check_login

# Utils
from utils import func

# Core
from core.config import ROLE_ADMIN, ROLE_USER
from core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("/{namespace}/blogs/create", response_model=Blog, status_code=status.HTTP_201_CREATED)
def create_new_blog(
    namespace: str,
    request: Request,
    response: Response,
    form_data: Annotated[BlogCreate, Form()],
    db: Database = Depends(get_mongo_db)
) -> Blog:
  """
  Create a new blog in the specified namespace.

  Args:
      namespace (str): The namespace to set for the database.
      request (Request): The FastAPI request object.
      response (Response): The FastAPI response object.
      form_data (BlogCreate): The blog data to create.
      db (Database): The MongoDB database instance.

  Returns:
      Blog: The newly created blog.
  """
  db = set_namespace(db, namespace)

  # Check login
  check_login(request, db, namespace, target_role=ROLE_ADMIN)

  storage_dir = func.get_root_path_project() / "storage" / namespace / 'blogs'
  storage_dir.mkdir(parents=True, exist_ok=True)

  filename = f'{func.random_string(10)}-{func.convert_filename(form_data.image.filename)}'
  file_path = storage_dir / filename
  with open(file_path, "wb") as f:
    f.write(form_data.image.file.read())

  form_data.image_url = f'{namespace}/images/blogs/{filename}'
  new_blog = crud_blog.create_blog(db=db, blog=form_data)
  return new_blog

@router.put("/{namespace}/blogs/{blog_id}/update", response_model=Blog, status_code=status.HTTP_201_CREATED)
def update_blog(
    namespace: str,
    request: Request,
    response: Response,
    blog_id: str,
    form_data: Annotated[BlogCreate, Form()],
    db: Database = Depends(get_mongo_db)
) -> Blog:
  """
  Update an existing blog in the specified namespace.

  Args:
      namespace (str): The namespace to set for the database.
      request (Request): The FastAPI request object.
      response (Response): The FastAPI response object.
      blog_id (str): The ID of the blog to update.
      form_data (BlogCreate): The updated blog data.
      db (Database): The MongoDB database instance.

  Returns:
      Blog: The updated blog.
  """
  db = set_namespace(db, namespace)

  # Check login
  check_login(request, db, namespace, target_role=ROLE_ADMIN)

  # Check if blog exists
  blog_row = crud_blog.get_blog(db=db, blog_id=blog_id)
  if not blog_row:
    raise HTTPException(status_code=404, detail="Blog not found")

  storage_dir = func.get_root_path_project() / "storage" / namespace / 'blogs'
  storage_dir.mkdir(parents=True, exist_ok=True)

  # Delete old image
  old_image_url = blog_row.image_url
  if old_image_url:
    old_image_path = storage_dir / old_image_url.split('/')[-1]
    if old_image_path.exists():
      old_image_path.unlink()

  # Upload new image
  filename = f'{func.random_string(10)}-{func.convert_filename(form_data.image.filename)}'
  file_path = storage_dir / filename
  with open(file_path, "wb") as f:
    f.write(form_data.image.file.read())

  form_data.image_url = f'{namespace}/images/blogs/{filename}'
  updated_blog = crud_blog.update_blog(db=db, blog_id=blog_id, blog=form_data)
  return updated_blog

@router.delete("/{namespace}/blogs/{blog_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(
    namespace: str,
    request: Request,
    response: Response,
    blog_id: str,
    db: Database = Depends(get_mongo_db)
) -> JSONResponse:
  """
  Delete an existing blog in the specified namespace.

  Args:
      namespace (str): The namespace to set for the database.
      request (Request): The FastAPI request object.
      response (Response): The FastAPI response object.
      blog_id (str): The ID of the blog to delete.
      db (Database): The MongoDB database instance.

  Returns:
      dict[str, str]: An empty dictionary.
  """
  db = set_namespace(db, namespace)

  # Check login
  check_login(request, db, namespace, target_role=ROLE_ADMIN)

  # Check if blog exists
  blog_row = crud_blog.get_blog(db=db, blog_id=blog_id)
  if not blog_row:
    raise HTTPException(status_code=404, detail="Blog not found")

  # Delete old image
  old_image_url = blog_row.image_url
  if old_image_url:
    storage_dir = func.get_root_path_project() / "storage" / namespace / 'blogs'
    old_image_path = storage_dir / old_image_url.split('/')[-1]
    if old_image_path.exists():
      old_image_path.unlink()

  crud_blog.delete_blog(db=db, blog_id=blog_id)

  return JSONResponse({
    "status": "success",
    "message": "Blog deleted successfully"
  })

@router.get("/{namespace}/blogs/list", response_model=List[Blog], status_code=status.HTTP_200_OK)
def get_blogs(
    namespace: str,
    request: Request,
    response: Response,
    skip: int = 0,
    limit: int = 100,
    db: Database = Depends(get_mongo_db)
) -> List[Blog]:
  """
  Retrieve a list of blogs from the specified namespace.

  Args:
      namespace (str): The namespace to set for the database.
      request (Request): The FastAPI request object.
      response (Response): The FastAPI response object.
      skip (int): The number of blogs to skip. Defaults to 0.
      limit (int): The maximum number of blogs to return. Defaults to 100.
      db (Database): The MongoDB database instance.

  Returns:
      List[Blog]: A list of blogs.
  """
  db = set_namespace(db, namespace)

  blogs = crud_blog.get_blogs(db=db, skip=skip, limit=limit)
  return blogs

@router.get("/{namespace}/blogs/{blog_id}", response_model=Blog, status_code=status.HTTP_200_OK)
def get_blog(
    namespace: str,
    request: Request,
    response: Response,
    blog_id: str,
    db: Database = Depends(get_mongo_db)
) -> Blog:
  """
  Retrieve an existing blog from the specified namespace.

  Args:
      namespace (str): The namespace to set for the database.
      request (Request): The FastAPI request object.
      response (Response): The FastAPI response object.
      blog_id (str): The ID of the blog to retrieve.
      db (Database): The MongoDB database instance.

  Returns:
      Blog: The blog.
  """
  db = set_namespace(db, namespace)

  # Check blog exists
  blog_row = crud_blog.get_blog(db=db, blog_id=blog_id)
  if not blog_row:
    raise HTTPException(status_code=404, detail="Collection not found")

  return blog_row
