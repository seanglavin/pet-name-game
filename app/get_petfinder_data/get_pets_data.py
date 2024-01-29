import httpx
import json
from app.get_petfinder_data.access_token import get_access_token
from app.get_petfinder_data.models import GetPetFinderDataRequest


PETFINDER_API_URL = "https://api.petfinder.com/v2/animals"


# ###
# ### Function for easy testing of different paramaters by editting the petfinder_data_request.json
# ### 
# async def load_test_parameters():
#     """
#     Load test parameters from the JSON file.
#     """
#     with open("app/get_petfinder_data/petfinder_data_request.json", "r") as file:
#         parameters = json.load(file)

#     # Create an instance of GetPetFinderDataRequest
#     request_instance = GetPetFinderDataRequest(**parameters)

#     # Return the flattened parameters serializable
#     return request_instance.model_dump(exclude_unset=True)


async def get_pets():
    """
    Load request parameters from the JSON file.
    Retrieve data from the PetFinder API based on the provided request

    Returns:
        dict: API response in JSON format.
    """

    # request = await load_test_parameters()

    with open("app/get_petfinder_data/petfinder_data_request.json", "r") as file:
        parameters = json.load(file)

    # Create an instance of GetPetFinderDataRequest
    request_instance = GetPetFinderDataRequest(**parameters)
    # Return the flattened parameters serializable
    request = request_instance.model_dump(exclude_unset=True)

    # Get a new access token
    access_token_data = await get_access_token()
    access_token = access_token_data.get("access_token", "")

    params = request
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    async with httpx.AsyncClient() as client:
        response = await client.get(PETFINDER_API_URL, params=params, headers=headers)

    if response.status_code == 200:
        return {"request": request_instance, "response": response.json()}
    else:
        return {"error": f"Error: {response.status_code}", "message": response.text}


async def validate_model_test_params():
    test_params = "app/get_petfinder_data/petfinder_data_request.json"

    with open(test_params, 'r') as file:
        parameters = json.load(file)

    print(f"Print#1 The test_params are: {parameters}")

    # try:
    # Create an instance of GetPetFinderDataRequest
    request_instance = GetPetFinderDataRequest(**parameters)
    # Convert validated instance to a dict
    validated_params = request_instance.model_dump(exclude_unset=True)
    print(f"Print#2 The validated_params are: {validated_params}")
    return validated_params
    # except ValidationError as e:
    #     print(f"Validation Error: {e.errors()}")