# Standard library imports
from contextlib import asynccontextmanager

# Third-party imports
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Local application imports
from core.logger import logging_config, get_logger
from db.mongodb import connect_to_mongo, close_mongo_connection
from core.config import APP_NAME, APP_DESCRIPTION, APP_VERSION, DEBUG
from api.v1.endpoints import item as item_endpoints

# Configure logging
logging_config()
logger = get_logger(__name__)

# Define application lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

# Initialize FastAPI application
app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    debug=DEBUG,
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(item_endpoints.router, prefix="/api/v1", tags=["items"])