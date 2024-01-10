from fastapi import FastAPI
import httpx
from app.get_petfinder_data.routes import router as get_pets_data_router


app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}

app.include_router(get_pets_data_router)