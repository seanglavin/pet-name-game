import json
from pydantic import ValidationError
from .models import GetPetFinderDataRequest


async def validate_model_test_params():
    test_params = "app/get_petfinder_data/test_params.json"

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