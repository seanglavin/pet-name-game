from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
import httpx
from app.get_petfinder_data.routes import router as get_pets_data_router
from app.database.session import get_db, engine
from app.config import settings
from sqlalchemy.orm import Session
import logging
from app.database.models import Base
from app.database.utils import create_db_and_tables

logger = logging.getLogger(__name__)


# def create_tables():
#     base = Base()
#     base.metadata.create_all(bind=engine)
#     print("Tables created successfully.")
#     logger.info("Tables created successfully.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # code to execute when app is loading
    for attr in dir(settings):
        if not attr.startswith("__"):
            value = getattr(settings, attr)
            print(f"{attr}: {value}")
    await create_db_and_tables(engine)
    yield
    # code to execute when app is shutting down


# def start_application():
app = FastAPI(
            title=settings.PROJECT_NAME,
            version=settings.PROJECT_VERSION,
            lifespan=lifespan
            )
    # create_tables()
    # app.include_router(get_pets_data_router)
    # return app

app.include_router(get_pets_data_router)
# app = start_application()


# @app.on_event("startup")
# async def on_startup():
#     await create_db_and_tables(engine)


@app.get("/", tags=["health"])
async def root():
    return dict(
        name=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        status="OK",
        message="Visit /docs for more information.",
    )


# app.include_router(get_pets_data_router)