from typing import Any
from pathlib import Path

from bson import ObjectId

from fastapi import FastAPI, Request
from fastapi import status

from starlette.responses import JSONResponse

from core.logger import get_logger

logger = get_logger(__name__)


def get_root_path_project() -> Path:
  """
  Get the root path of the project.

  Returns:
      Path: The root path of the project.
  """
  return Path(__file__).resolve().parent.parent


def convert_object_id_to_str(obj: Any) -> str:
  """
  Convert an ObjectId to a string.
  Args:
      obj: The object to convert.

  Returns:
      str: The string representation of the ObjectId.
  """
  if isinstance(obj, ObjectId):
    return str(obj)
  # Handle other types if necessary, though for this case ObjectId is main concern
  raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def convert_object_id_of_item(obj: Any) -> any:
  """
  Convert an ObjectId to a string.
  Args:
      obj: The object to convert.

  Returns:
      any: The string representation of the ObjectId.
  """

  if '_id' in obj:
    obj['_id'] = convert_object_id_to_str(obj['_id'])
  return obj


def unauthorized_response() -> JSONResponse:
  return JSONResponse({"detail": "Invalid or expired token"}, status_code=status.HTTP_401_UNAUTHORIZED)


def get_client_ip(request: Request) -> dict:
  client_ip = request.headers.get("X-Forwarded-For") or request.client.host
  return {"client_ip": client_ip}


def get_device(request: Request) -> dict:
  device = request.headers.get("User-Agent")
  return {"device": device}

def convert_username(username: str) -> str:
  username = username.lower().strip()
  return username
