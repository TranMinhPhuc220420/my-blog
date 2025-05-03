from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from cryptography.fernet import Fernet

from core.config import FERNET_KEY, JWT_SECRET_KEY, JWT_ALGORITHM, JWT_ACCESS_TOKEN_EXPIRE_MINUTES
from core.config import JWT_REFRESH_SECRET_KEY, JWT_REFRESH_TOKEN_EXPIRE_MINUTES

from core.logger import get_logger

logger = get_logger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
  return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None):
  to_encode = data.copy()
  expire = datetime.utcnow() + (expires_delta or timedelta(seconds=JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
  to_encode.update({"exp": expire})
  return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def create_refresh_token(data: dict, expires_delta: timedelta = None):
  to_encode = data.copy()
  expire = datetime.utcnow() + (expires_delta or timedelta(seconds=JWT_REFRESH_TOKEN_EXPIRE_MINUTES))
  to_encode.update({"exp": expire})
  return jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, algorithm=JWT_ALGORITHM)


def verify_access_token(token: str):
  return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])


def verify_refresh_token(token: str):
  return jwt.decode(token, JWT_REFRESH_SECRET_KEY, algorithms=[JWT_ALGORITHM])


def hash_password(password: str) -> str:
  """
  Hash a password using bcrypt.

  Args:
      password (str): The password to hash.

  Returns:
      str: The hashed password.
  """

  return pwd_context.hash(password)


def encrypt_access_token(access_token: str) -> str:
  fernet = Fernet(FERNET_KEY)

  encrypted_token = fernet.encrypt(access_token.encode()).decode()

  return encrypted_token


def decrypt_access_token(encrypted_token: str) -> str:
  fernet = Fernet(FERNET_KEY)

  # Check encrypted_token is valid
  try:
    decrypted_token = fernet.decrypt(encrypted_token.encode()).decode()
  except BaseException as e:
    logger.warn('Encrypted token is not valid or has been modified')
    return encrypted_token

  return decrypted_token
