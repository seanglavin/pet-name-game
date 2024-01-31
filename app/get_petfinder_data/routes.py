from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.get_petfinder_data.get_pets_data import get_pets, validate_model_test_params
from app.get_petfinder_data.models import PetfinderAnimalsDataDumpResponse
from app.database.crud import save_petfinder_data, get_petfinder_animals, get_response_data, delete_all_petfinder_data
from pydantic import ValidationError


router = APIRouter(prefix="/data", tags=["data"])


async def handle_http_response(response):
    """
    Handle HTTP response and return appropriate result.

    Args:
        response: HTTP response object from an asynchronous HTTP client.

    Returns:
        dict: If status code is 200, return JSON response.
        dict: If status code is not 200, return error details.
    """
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Error: {response.status_code}", "message": response.text}



@router.post("/petfinder_animals")
async def get_and_save_petfinder_data_dump(db: AsyncSession = Depends(get_db)):
    try:
        pets_data = await get_pets()

        # Extract request parameters and response data from pets_data
        api_response_data = pets_data.get("response")
        request_parameters = pets_data.get("request")

        # Save pets data to the database
        saved_data = await save_petfinder_data(db, response_data = api_response_data, request = request_parameters)

        return {"message": "Data saved successfully", "saved_data": saved_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    

@router.get("/petfinder_animals/all", response_model=List[PetfinderAnimalsDataDumpResponse])
async def read_petfinder_animals(db: AsyncSession = Depends(get_db)):
    """
    Retrieve all PetfinderAnimalsDataDump entries.

    Args:
        limit: Maximum number of records to retrieve.
        db: SQLAlchemy database session.

    Returns:
        List of PetfinderAnimalsDataDump objects.
    """
    return await get_petfinder_animals(db)


@router.get("/petfinder_animals/{petfinder_animals_data_dump_id}/response_data")
async def read_response_data(petfinder_animals_data_dump_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve response data for a specific PetfinderAnimalsDataDump entry.

    Args:
        petfinder_animals_data_dump_id: ID of the PetfinderAnimalsDataDump object.
        db: SQLAlchemy database session.

    Returns:
        Dictionary containing response data.
    """
    response_data = await get_response_data(db, petfinder_animals_data_dump_id)
    if response_data:
        return response_data
    else:
        raise HTTPException(status_code=404, detail="Response data not found")






@router.get("/validate_test_params")
async def validate_test_params_endpoint():
    try:
        response = await validate_model_test_params()
        return response
    except ValidationError as e:
        error_messages = e.errors()
        error_response = {"error": "Validation Error", "detail": error_messages}
        raise HTTPException(status_code=422, detail=error_response)
    

@router.delete("/petfinder_animals")
async def delete_petfinder_data_dump_table_contents(db: AsyncSession = Depends(get_db)):
    response = await delete_all_petfinder_data(db)
    return {f"Table entries deleted: {response}"}