from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from app.get_petfinder_data.routes import router as get_pets_data_router
from app.database.session import get_db, engine
from sqlmodel.ext.asyncio.session import AsyncSession
from app.config import settings
import logging
from app.database.utils import create_db_and_tables
import asyncio


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # code to execute when app is loading place above "yield"
    # for attr in dir(settings):
    #     if not attr.startswith("__"):
    #         value = getattr(settings, attr)
    #         print(f"{attr}: {value}")
    # await asyncio.sleep(2)

    # # NO LONGER CREATE DB AT STARTUP, USE ALEMBIC
    # await create_db_and_tables(engine)
    yield
    # code to execute when app is shutting down place under "yield"



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