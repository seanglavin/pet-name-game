from fastapi import FastAPI, Depends
import httpx
from app.get_petfinder_data.routes import router as get_pets_data_router
from app.database.session import get_db, engine, Base
from app.config import settings
from sqlalchemy.orm import Session



def create_tables():         
	Base.metadata.create_all(bind=engine)

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