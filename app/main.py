from fastapi import FastAPI, Depends
import httpx
from app.get_petfinder_data.routes import router as get_pets_data_router
from app.database.session import get_db, engine
from app.config import settings
from sqlalchemy.orm import Session
import logging
from app.database.models import PetfinderAnimals

logger = logging.getLogger(__name__)


def create_tables():
    MetaData = PetfinderAnimals.metadata  
    try:
        MetaData.create_all(bind=engine)
        print("Tables created successfully.")
        logger.info("Tables created successfully.")
    except Exception as e:
        print("Error creating tables:", e)
        logger.info("Error creating tables.")

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,
                  version=settings.PROJECT_VERSION
                  )
    create_tables()
    return app

app = start_application()


@app.get("/")
async def root(db: Session = Depends(get_db)):
    return {"Hello": "World"}

app.include_router(get_pets_data_router)