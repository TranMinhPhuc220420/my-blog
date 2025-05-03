# server/core/middleware.py

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import status

from core.security import decrypt_access_token, verify_access_token
from core.config import (
  KEY_ACCESS_TOKEN, INVALID_ACCESS_TOKEN_ERROR_CODE,
  EXPIRED_ACCESS_TOKEN_ERROR_CODE, BAD_REQUEST_ERROR_CODE,
)

from core.logger import get_logger

logger = get_logger(__name__)


def process_response(request) -> Request:
  # Auth by access token bearer
  auth_header = request.headers.get("Authorization")
  # Auth by cookie
  encrypt_access_token_raw = request.cookies.get(KEY_ACCESS_TOKEN)

  access_token = None
  payload = None

  if auth_header:
    scheme, access_token_raw = auth_header.split()
    if scheme.lower() != "bearer":
      raise ValueError("Invalid scheme")
    if not access_token_raw or len(access_token_raw.split(".")) != 3:
      raise ValueError("Invalid access token")
    access_token = decrypt_access_token(access_token_raw)
  elif encrypt_access_token_raw:
    access_token = decrypt_access_token(encrypt_access_token_raw)

  if access_token is not None:
    payload = verify_access_token(access_token)

  # logger.info(access_token)
  # logger.info(payload)
  request.state.jwt_payload = payload

  return request


class AuthMiddleware(BaseHTTPMiddleware):
  async def dispatch(self, request: Request, call_next):

    try:
      process_response(request)
    except (ValueError, ExpiredSignatureError) as e:
      return JSONResponse({"error_code": EXPIRED_ACCESS_TOKEN_ERROR_CODE, "error": str(e)}, status_code=status.HTTP_401_UNAUTHORIZED)
    except (ValueError, JWTError) as e:
      return JSONResponse({"error_code": INVALID_ACCESS_TOKEN_ERROR_CODE, "error": str(e)}, status_code=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
      return JSONResponse({"error_code": BAD_REQUEST_ERROR_CODE, "error": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

    return await call_next(request)

