import requests
from app.dependencies import get_petfinder_access_token


PETFINDER_API_URL = "https://api.petfinder.com/v2/animals"

def get_cats(limit=10):
    """
    Retrieve a list of cats from the PetFinder API.

    Args:
        api_key (str): PetFinder API key.
        access_token (str): PetFinder API access token.
        limit (int): Maximum number of results to return per 'page' response.

    Returns:
        dict: API response in JSON format.
    """
    # Get a new access token
    access_token_data = get_petfinder_access_token()
    access_token = access_token_data.get("access_token", "")

    params = {"type": "cat", "limit": limit}
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    response = requests.get(PETFINDER_API_URL, params=params, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Error: {response.status_code}", "message": response.text}
