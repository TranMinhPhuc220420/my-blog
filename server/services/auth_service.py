from fastapi import Request

from core import security
from core.config import ROLE_ADMIN

from crud.user import get_user, get_user_by_username, set_refresh_token_for_user, set_info_login, remove_info_login
from fastapi import HTTPException, status

from pymongo.database import Database
from db.mongodb import set_namespace

from core.logger import get_logger

logger = get_logger(__name__)


def authenticate_user(
    db: Database,
    username: str,
    password: str
):
  """
  Get user by username and password
  Args:
    db (Database): The MongoDB database instance.
    username (str): Username of user
    password (str): Password of user

  Returns:
    User: User object
  """
  user = get_user_by_username(db, username)

  if not user or not security.verify_password(password, user.hashed_password):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

  return user


def create_access_token_by_username_password(
    db: Database,
    username: str,
    password: str,
    info_login: dict = None
) -> tuple[str, str]:
  """
  Create access token and refresh token by username and password
  Args:
    db (Database): The MongoDB database instance.
    username (str): Username of user
    password (str): Password of user
    info_login (dict): Device info

  Returns:
    tuple[str, str]: Access token and refresh token
  """
  user = authenticate_user(db, username, password)
  payload = {"username": user.username}

  access_token = security.create_access_token(data=payload)
  refresh_token = security.create_refresh_token(data=payload)

  # Update refresh token
  set_refresh_token_for_user(db, user.id, refresh_token)

  if info_login:
    set_info_login(db, user.id, info_login)

  return access_token, refresh_token


def create_access_token_by_refresh_access_token(
    db: Database,
    current_refresh_token: str,
    info_login: dict
) -> tuple[str, str]:
  """
  Create access token and refresh token by refresh token
  Args:
    db (Database): The MongoDB database instance.
    current_refresh_token (str): Current refresh token
    info_login (dict): Device info

  Returns:
    tuple[str, str]: Access token and refresh token
  """
  payload = security.verify_refresh_token(current_refresh_token)
  if payload is None:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

  username = payload['username']

  # Check if user exists and then check refresh token and device info is valid
  user = get_user_by_username(db, username)
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
  if user.refresh_token != current_refresh_token:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
  if user.device_info != info_login:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid device info")

  # Create new access token and refresh token
  access_token = security.create_access_token(data=payload)
  refresh_token = security.create_refresh_token(data=payload)

  # Update refresh token
  set_refresh_token_for_user(db, user.id, refresh_token)
  # Update device info
  set_info_login(db, user.id, info_login)

  return access_token, refresh_token


def check_login(
    request: Request,
    db: Database,
    namespace: str,
    target_role: str = None,
) -> bool:
  """
  Check if user is logged in
  Args:
    request (Request): The FastAPI request object.
    db (Database): The MongoDB database instance.
    namespace (str): The namespace to set for the database.
    target_role (str, optional): The role to check. Defaults to None.

  Returns:
    bool: True if user is logged in
  """
  jwt_payload = request.state.jwt_payload

  if not jwt_payload:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated or token expired")

  db = set_namespace(db, namespace)
  username = jwt_payload['username']
  user_item = get_user_by_username(db, username)

  if not user_item:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

  request.state.auth = user_item

  if target_role:
    if user_item.role != target_role:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to perform this action")

  return True


def handle_logout(
    request: Request,
    db: Database,
):
  auth = request.state.auth
  remove_info_login(db, auth.id)
