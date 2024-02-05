from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import ValidationError
import logging

from app.database.session import get_db
from app.get_petfinder_data.get_pets_data import get_pets, validate_model_test_params
from app.database.models import PetfinderAnimalsDataDump, PetfinderAnimalsDataDumpResponse, ResponseDataRead
from app.database.crud import save_petfinder_data, get_petfinder_animals, get_response_data_by_dump_id, get_response_data_by_batch_id, delete_all_petfinder_data


logger = logging.getLogger(__name__)

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



@router.post("/petfinder_animals_dump")
async def get_and_save_petfinder_data_dump(db: AsyncSession = Depends(get_db)):
    try:
        pets_data = await get_pets(db)
        print("Petfinder Data Dumped: Success!")
        return pets_data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    

@router.get("/petfinder_animals_dump", response_model=List[PetfinderAnimalsDataDumpResponse])
async def read_petfinder_animals(db: AsyncSession = Depends(get_db)):
    """
    Retrieve all PetfinderAnimalsDataDump entries.

    Args:
        limit: Maximum number of records to retrieve.
        db: SQLAlchemy database session.

    Returns:
        List of PetfinderAnimalsDataDump objects.
    """
    try:
        result = await get_petfinder_animals(db)
        return result
    
    except HTTPException as http_exception:
        raise http_exception
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.get("/petfinder_animals_dump/animals/dump_id/{petfinder_animals_data_dump_id}")
async def read_response_data_by_dump_id(petfinder_animals_data_dump_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve response data for a specific PetfinderAnimalsDataDump entry.

    Args:
        petfinder_animals_data_dump_id: ID of the PetfinderAnimalsDataDump object.
        db: SQLAlchemy database session.

    Returns:
        List of Animals for specified data dump id
    """
    response_data = await get_response_data_by_dump_id(petfinder_animals_data_dump_id, db)

    if response_data:
        return response_data
    
    else:
        raise HTTPException(status_code=404, detail=f"No animals found for data dump id: {petfinder_animals_data_dump_id}")


@router.get("/petfinder_animals_dump/animals/batch_id/{petfinder_animals_batch_id}")
async def read_response_data_by_batch_id(petfinder_animals_batch_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve response data for a specific PetfinderAnimalsDataDump entry.

    Args:
        petfinder_animals_data_dump_id: ID of the PetfinderAnimalsDataDump batch of objects.
        db: SQLAlchemy database session.

    Returns:
        List of Animals for specified data dump request batch id
    """
    response_data = await get_response_data_by_batch_id(petfinder_animals_batch_id, db)

    if response_data:
        return response_data
    
    else:
        raise HTTPException(status_code=404, detail=f"No animals found for data dump request batch id: {request_batch_id}")





@router.get("/validate_test_params")
async def validate_test_params_endpoint():
    try:
        response = await validate_model_test_params()
        return response
    
    except ValidationError as e:
        error_messages = e.errors()
        error_response = {"error": "Validation Error", "detail": error_messages}
        raise HTTPException(status_code=422, detail=error_response)
    

@router.delete("/petfinder_animals_dump")
async def delete_petfinder_data_dump_table_contents(db: AsyncSession = Depends(get_db)):
    response = await delete_all_petfinder_data(db)
    return {f"Table entries deleted: {response}"}