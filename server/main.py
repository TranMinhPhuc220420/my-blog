# ─── Standard Library ──────────────────────────────────────────────
from contextlib import asynccontextmanager

# ─── Third-party ───────────────────────────────────────────────────
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware import Middleware

# ─── Local Imports ─────────────────────────────────────────────────
from db.mongodb import connect_to_mongo, close_mongo_connection
from core.config import APP_NAME, APP_DESCRIPTION, APP_VERSION, DEBUG
from core.logger import logging_config, get_logger
from core.middleware import AuthMiddleware
from api.v1.endpoints import (
  item as item_endpoints,
  websocket as websocket_endpoints,
  auth as auth_endpoints,
  category as category_endpoints,
  blog as blog_endpoints,
  images as images_endpoints,
)

# ─── Logger Setup ──────────────────────────────────────────────────
logging_config()
logger = get_logger(__name__)


# ─── Application Lifespan ──────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
  await connect_to_mongo()
  yield
  await close_mongo_connection()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

# ─── App Initialization ────────────────────────────────────────────
app = FastAPI(
  title=APP_NAME,
  description=APP_DESCRIPTION,
  version=APP_VERSION,
  debug=DEBUG,
  lifespan=lifespan,

  middleware=[
    Middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"]),
    Middleware(AuthMiddleware),
  ]
)

# ─── Static Files ──────────────────────────────────────────────────
app.mount("/static", StaticFiles(directory="static"), name="static")

# ─── Routers ───────────────────────────────────────────────────────
app.include_router(images_endpoints.router, tags=["items"])
app.include_router(item_endpoints.router, prefix="/api/v1", tags=["items"])
app.include_router(websocket_endpoints.router, prefix="/api/v1", tags=["websocket"])
app.include_router(auth_endpoints.router, prefix="/api/v1", tags=["auth"])
app.include_router(category_endpoints.router, prefix="/api/v1", tags=["category"])
app.include_router(blog_endpoints.router, prefix="/api/v1", tags=["blog"])
