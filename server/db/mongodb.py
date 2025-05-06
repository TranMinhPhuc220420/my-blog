from pymongo.database import Database
from pymongo import MongoClient
from core.config import MONGO_DB_URL, MONGO_NAMESPACE_DEFAULT
from motor.motor_asyncio import AsyncIOMotorClient

from core.logger import get_logger

logger = get_logger(__name__)

client: MongoClient = None
db: Database = None


async def connect_to_mongo() -> bool:
  '''
  Connects to MongoDB using the provided URL and database name.

  Returns:
      bool: True if the connection was established successfully, False otherwise.
  '''
  global client, db
  if client is None:
    try:
      client = MongoClient(MONGO_DB_URL)
      db = client[MONGO_NAMESPACE_DEFAULT]

      logger.info(f'MONGO_DB_URL={MONGO_DB_URL}')
      logger.info(f'MONGO_NAMESPACE_DEFAULT={MONGO_NAMESPACE_DEFAULT}')
      logger.info("Connected to MongoDB!")
      # client.admin.command('ping')

      return True

    except Exception as e:
      logger.error(f"Error connecting to MongoDB: {e}")
      client = None
      db = None

  return False


async def close_mongo_connection() -> bool:
  '''
  Closes the MongoDB client connection and clears the global 'client' and 'db' variables

  Returns:
      bool: True if the connection was closed successfully, False otherwise.
  '''
  global client, db
  if client:
    client.close()
    client = None
    db = None

    logger.info("MongoDB connection closed.")
    return True

  logger.error("MongoDB client is not initialized. Cannot close connection.")
  return False


def get_mongo_db() -> Database:
  '''
  Retrieves the current MongoDB database connection.

  Returns:
      Database: The MongoDB database object.

  Raises:
      ConnectionError: If the MongoDB connection cannot be established.
  '''
  global db

  if db is None:
    connect_to_mongo()

  if db is None:
    raise ConnectionError(f'MongoDB connection is not established. {MONGO_DB_URL} {MONGO_NAMESPACE_DEFAULT}')

  return db


def set_namespace(db_current: Database, namespace: str) -> Database:
  '''
  Sets the namespace (database) for the current MongoDB connection.

  Args:
      db_current (Database): The current MongoDB database object.
      namespace (str): The name of the database to switch to.

  Returns:
      Database: The MongoDB database object.
  '''

  global client
  if client:

    db_current = client[namespace]
    logger.info(f"Changed MongoDB database to {namespace}")

    return db_current
  else:
    logger.error("MongoDB client is not initialized. Cannot change database name.")
    return None
