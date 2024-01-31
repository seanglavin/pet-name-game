from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from app.get_petfinder_data.routes import router as get_pets_data_router
from app.database.session import get_db, engine
from app.config import settings
import logging
from app.database.utils import create_db_and_tables
import asyncio


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # code to execute when app is loading
    # for attr in dir(settings):
    #     if not attr.startswith("__"):
    #         value = getattr(settings, attr)
    #         print(f"{attr}: {value}")
    await asyncio.sleep(3)
    await create_db_and_tables(engine)
    yield
    # code to execute when app is shutting down



app = FastAPI(
            title=settings.PROJECT_NAME,
            version=settings.PROJECT_VERSION,
            lifespan=lifespan
            )


app.include_router(get_pets_data_router)


@app.get("/", tags=["health"])
async def root():
    return dict(
        name=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        status="OK",
        message="Visit /docs for more information.",
    )