from fastapi import APIRouter, HTTPException
from app.get_petfinder_data.get_pets_data import get_pets
from app.get_petfinder_data.validate_input import validate_model_test_params
from pydantic import ValidationError

router = APIRouter(prefix="/get_data", tags=["get_data"])

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




@router.get("/get_pets")
async def get_pets_endpoint():
    response = await get_pets()
    return response


@router.get("/validate_test_params")
async def validate_test_params_endpoint():
    try:
        response = await validate_model_test_params()
        return response
    except ValidationError as e:
        error_messages = e.errors()
        error_response = {"error": "Validation Error", "detail": error_messages}
        raise HTTPException(status_code=422, detail=error_response)