# Standard libraries
from typing import List, Annotated

# FastAPI libraries
from fastapi import Request, Response, status, APIRouter, Depends, HTTPException
from fastapi import Form

# MongoDB
from pymongo.database import Database

from crud.user import get_user_by_username
from db.mongodb import get_mongo_db, set_namespace
from schemas.auth import User, LoginRequest, TokenResponse, RegisterRequest, SetRoleRequest
from crud import user as crud_user

# Services
from services.auth_service import (check_login, handle_logout,
                                   create_access_token_by_username_password,
                                   create_access_token_by_refresh_access_token
                                   )

# Utils
from utils import func

# Core
from core.config import KEY_TOKEN_TYPE, KEY_ACCESS_TOKEN, KEY_REFRESH_TOKEN, ROLE_ADMIN
from core.security import encrypt_access_token, decrypt_access_token
from core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("/{namespace}/register", response_model=User, status_code=status.HTTP_201_CREATED)
def user_register(
    namespace: str,
    form_data: Annotated[RegisterRequest, Form()],
    db: Database = Depends(get_mongo_db)
) -> User:
  db = set_namespace(db, namespace)

  username = form_data.username
  password = form_data.password

  user_exists = get_user_by_username(db, username)
  if user_exists:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

  new_item = crud_user.create_user(db=db, username=username, password=password)
  return new_item


@router.post("/{namespace}/login", response_model=TokenResponse)
def user_login(
    namespace: str,
    form_data: Annotated[LoginRequest, Form()],
    request: Request,
    response: Response,
    db=Depends(get_mongo_db)
):
  db = set_namespace(db, namespace)

  username = form_data.username
  password = form_data.password
  client_ip = func.get_client_ip(request)
  device = func.get_device(request)

  info_login = {
    **client_ip,
    **device
  }

  access_token, refresh_access_token = create_access_token_by_username_password(db, username, password,
                                                                                info_login=info_login)

  response.set_cookie(
    key=KEY_REFRESH_TOKEN,
    value=encrypt_access_token(refresh_access_token),
    httponly=True,
    secure=False,
    samesite="lax",
    max_age=900,
    path="/"
  )

  return {
    KEY_ACCESS_TOKEN: encrypt_access_token(access_token),
    KEY_TOKEN_TYPE: "bearer"
  }


@router.post("/{namespace}/logout")
async def user_logout(
    request: Request,
    response: Response,
    namespace: str,
    db: Database = Depends(get_mongo_db)
):
  set_namespace(db, namespace)

  check_login(request, db, namespace)

  handle_logout(request, db)

  response.delete_cookie(KEY_REFRESH_TOKEN)

  return {
    KEY_ACCESS_TOKEN: None,
    KEY_TOKEN_TYPE: None
  }


@router.post("/{namespace}/refresh-token")
async def user_refresh_token(
    request: Request,
    response: Response,
    namespace: str,
    db: Database = Depends(get_mongo_db)
):
  db = set_namespace(db, namespace)

  refresh_access_token_raw = request.cookies.get(KEY_REFRESH_TOKEN)
  if not refresh_access_token_raw:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated or token expired")

  client_ip = func.get_client_ip(request)
  device = func.get_device(request)
  info_login = {
    **client_ip,
    **device
  }

  refresh_access_token = decrypt_access_token(refresh_access_token_raw)
  access_token, refresh_access_token = create_access_token_by_refresh_access_token(db, refresh_access_token, info_login)

  response.set_cookie(
    key=KEY_REFRESH_TOKEN,
    value=encrypt_access_token(refresh_access_token),
    httponly=True,
    secure=False,
    samesite="lax",
    max_age=900,
    path="/"
  )

  return {
    KEY_ACCESS_TOKEN: encrypt_access_token(access_token),
    KEY_TOKEN_TYPE: "bearer"
  }


@router.put("/{namespace}/set-role", response_model=User, status_code=status.HTTP_200_OK)
def user_set_role(
    namespace: str,
    request: Request,
    response: Response,
    form_data: Annotated[SetRoleRequest, Form()],
    db: Database = Depends(get_mongo_db)
) -> User:
  db = set_namespace(db, namespace)

  # Check login
  check_login(request, db, namespace, target_role=ROLE_ADMIN)

  role = form_data.target_role
  user_id = form_data.user_id

  # Check user exists
  user_item = crud_user.get_user(db, user_id)
  if not user_item:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

  crud_user.set_role_for_user(db, user_id, role)

  user = crud_user.get_user(db, user_id)
  return user


@router.get("/{namespace}/me", response_model=User, status_code=status.HTTP_200_OK)
def user_get_me(
    request: Request,
    namespace: str,
    db: Database = Depends(get_mongo_db),
) -> User:
  # Check if the user is logged in
  check_login(request, db, namespace)

  auth = request.state.auth
  return auth


@router.get("/{namespace}/users", response_model=List[User], status_code=status.HTTP_200_OK)
def get_users(
    namespace: str,
    skip: int = 0,
    limit: int = 100,
    db: Database = Depends(get_mongo_db)
) -> List[User]:
  """
  Retrieve a list of users from the specified namespace.

  Args:
      namespace (str): The namespace to set for the database.
      skip (int): The number of items to skip. Defaults to 0.
      limit (int): The maximum number of items to return. Defaults to 100.
      db (Database): The MongoDB database instance.

  Returns:
      List[User]: A list of users.
  """
  db = set_namespace(db, namespace)
  users = crud_user.get_users(db=db, skip=skip, limit=limit)
  return users
