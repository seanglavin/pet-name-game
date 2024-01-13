import requests
import httpx
import json
from app.petfinder_auth.access_token import get_access_token
from app.get_petfinder_data.models import GetPetFinderDataRequest


PETFINDER_API_URL = "https://api.petfinder.com/v2/animals"


###
### Function for easy testing of different paramaters by editting the test_params.json
### 
async def load_test_parameters():
    """
    Load test parameters from the JSON file.
    """
    with open("app/get_petfinder_data/test_params.json", "r") as file:
        parameters = json.load(file)

    # Create an instance of GetPetFinderDataRequest
    request_instance = GetPetFinderDataRequest(**parameters)

    # Return the flattened parameters serializable
    return request_instance.model_dump(exclude_unset=True)


###
### When not testing uncomment other function that takes the model
###
# def get_pets(request: GetPetFinderDataRequest):
async def get_pets():
    """
    Retrieve data from the PetFinder API based on the provided request

    Args:
        request (GetPetFinderDataRequest): Pydantic model representing the request parameters.

    Returns:
        dict: API response in JSON format.
    """
    # Load test parameters
    request = await load_test_parameters()

    # Get a new access token
    access_token_data = await get_access_token()
    access_token = access_token_data.get("access_token", "")

    params = request
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    async with httpx.AsyncClient() as client:
        response = await client.get(PETFINDER_API_URL, params=params, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Error: {response.status_code}", "message": response.text}
