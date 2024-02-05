import httpx
import json
from sqlmodel.ext.asyncio.session import AsyncSession
from app.get_petfinder_data.access_token import get_access_token
from app.get_petfinder_data.models import GetPetFinderDataRequest
from app.database.crud import get_largest_request_batch_id, save_petfinder_data


PETFINDER_API_URL = "https://api.petfinder.com/v2/animals"


async def get_pets(db: AsyncSession):
    """
    Load request parameters from the JSON file.
    Retrieve data from the PetFinder API based on the provided request

    Returns:
        dict: API response in JSON format.
    """

    request_batch_id = await get_largest_request_batch_id(db) + 1

    with open("app/get_petfinder_data/petfinder_data_request.json", "r") as file:
        parameters = json.load(file)

    # Create an instance of GetPetFinderDataRequest and then dump to serialize it
    request_instance = GetPetFinderDataRequest(**parameters)
    request = request_instance.model_dump(exclude_unset=True)

    # Get a new access token
    access_token_data = await get_access_token()
    access_token = access_token_data.get("access_token", "")

    params = request
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    async with httpx.AsyncClient() as client:
        response = await client.get(PETFINDER_API_URL, params=params, headers=headers)

        if response.status_code == 200:
            total_count = response.json().get("pagination", {}).get("total_count")
            total_pages = response.json().get("pagination", {}).get("total_pages")

            # Save first page of data
            await save_petfinder_data(db, response.json(), request_instance, request_batch_id)
            print(f"Page: {request_instance.page} of {total_pages} loaded.")


            # Save the rest of the pages
            for page_num in range(2, total_pages + 1):
                request_instance.page = page_num
                params = request_instance.model_dump(exclude_unset=True)
                response = await client.get(PETFINDER_API_URL, params=params, headers=headers)
                await save_petfinder_data(db, response.json(), request_instance, request_batch_id)
                print(f"Page: {request_instance.page} of {total_pages} loaded.")

            return {"request_batch_id": request_batch_id, "pages_loaded": total_pages, "total_count": total_count}
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