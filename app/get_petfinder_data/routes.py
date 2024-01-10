from fastapi import APIRouter
from app.get_petfinder_data.get_pets_data import get_cats

router = APIRouter(prefix="/get_data", tags=["get_data"])

@router.get("/get_cats")
async def get_cats_endpoint():
    cats_data = get_cats()
    return cats_data
