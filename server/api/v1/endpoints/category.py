# Standard libraries
from typing import List, Annotated
from starlette.responses import JSONResponse

# FastAPI libraries
from fastapi import APIRouter, Depends, HTTPException
from fastapi import Request, Response, status
from fastapi import Form

# MongoDB
from pymongo.database import Database
from db.mongodb import get_mongo_db, set_namespace
from schemas.category import CategoryCreate, Category
from crud import category as crud_category
from services.auth_service import check_login

# Utils
from utils import func

# Core
from core.config import ROLE_ADMIN, ROLE_USER
from core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("/{namespace}/categories/create", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_new_category(
    namespace: str,
    request: Request,
    response: Response,
    form_data: Annotated[CategoryCreate, Form()],
    db: Database = Depends(get_mongo_db)
) -> Category:
  """
  Create a new category in the specified namespace.

  Args:
      namespace (str): The namespace to set for the database.
      request (Request): The FastAPI request object.
      response (Response): The FastAPI response object.
      form_data (CategoryCreate): The category data to create.
      db (Database): The MongoDB database instance.

  Returns:
      Category: The newly created category.
  """
  db = set_namespace(db, namespace)

  # Check login
  check_login(request, db, namespace, target_role=ROLE_ADMIN)

  new_category = crud_category.create_category(db=db, category=form_data)
  return new_category


@router.put("/{namespace}/categories/{category_id}/update", response_model=Category,
            status_code=status.HTTP_201_CREATED)
def update_category(
    namespace: str,
    request: Request,
    response: Response,
    category_id: str,
    form_data: Annotated[CategoryCreate, Form()],
    db: Database = Depends(get_mongo_db)
) -> Category:
  """
  Update an existing category in the specified namespace.

  Args:
      namespace (str): The namespace to set for the database.
      request (Request): The FastAPI request object.
      response (Response): The FastAPI response object.
      category_id (str): The ID of the category to update.
      form_data (CategoryCreate): The updated category data.
      db (Database): The MongoDB database instance.

  Returns:
      Category: The updated category.
  """
  db = set_namespace(db, namespace)

  # Check login
  check_login(request, db, namespace, target_role=ROLE_ADMIN)

  # Check if category exists
  if crud_category.get_category(db=db, category_id=category_id) is None:
    raise HTTPException(status_code=404, detail="Category not found")

  updated_category = crud_category.update_category(db=db, category_id=category_id, category=form_data)
  return updated_category


@router.delete("/{namespace}/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    namespace: str,
    request: Request,
    response: Response,
    category_id: str,
    db: Database = Depends(get_mongo_db)
) -> JSONResponse:
  """
  Delete an existing category in the specified namespace.

  Args:
      namespace (str): The namespace to set for the database.
      request (Request): The FastAPI request object.
      response (Response): The FastAPI response object.
      category_id (str): The ID of the category to delete.
      db (Database): The MongoDB database instance.

  Returns:
      dict[str, str]: An empty dictionary.
  """
  db = set_namespace(db, namespace)

  # Check login
  check_login(request, db, namespace, target_role=ROLE_ADMIN)

  # Check if category exists
  if crud_category.get_category(db=db, category_id=category_id) is None:
    raise HTTPException(status_code=404, detail="Category not found")

  crud_category.delete_category(db=db, category_id=category_id)

  return JSONResponse({
    "status": "success",
    "message": "Category deleted successfully"
  })


@router.get("/{namespace}/categories/list", response_model=List[Category], status_code=status.HTTP_200_OK)
def get_categories(
    namespace: str,
    request: Request,
    response: Response,
    skip: int = 0,
    limit: int = 100,
    db: Database = Depends(get_mongo_db)
) -> List[Category]:
  """
  Retrieve a list of categories from the specified namespace.

  Args:
      namespace (str): The namespace to set for the database.
      request (Request): The FastAPI request object.
      response (Response): The FastAPI response object.
      skip (int): The number of categories to skip. Defaults to 0.
      limit (int): The maximum number of categories to return. Defaults to 100.
      db (Database): The MongoDB database instance.

  Returns:
      List[Category]: A list of categories.
  """
  db = set_namespace(db, namespace)

  categories = crud_category.get_categories(db=db, skip=skip, limit=limit)
  return categories


@router.get("/{namespace}/categories/{category_id}", response_model=Category, status_code=status.HTTP_200_OK)
def get_category(
    namespace: str,
    category_id: str,
    db: Database = Depends(get_mongo_db)
) -> Category:
  """
  Retrieve a specific category by its ID from the specified namespace.

  Args:
      namespace (str): The namespace to set for the database.
      category_id (str): The ID of the category to retrieve.
      db (Database): The MongoDB database instance.

  Returns:
      Category: The requested category.

  Raises:
      HTTPException: If the Category is not found.
  """
  db = set_namespace(db, namespace)
  category = crud_category.get_category(db=db, category_id=category_id)
  if category is None:
    raise HTTPException(status_code=404, detail="Category not found")
  return category
