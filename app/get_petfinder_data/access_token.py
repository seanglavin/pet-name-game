import requests
import httpx
from app.config import settings


PETFINDER_API_KEY = settings.PETFINDER_API_KEY
PETFINDER_API_SECRET = settings.PETFINDER_API_SECRET


async def get_access_token():

    """
    Get a new access token from the PetFinder API using client credentials.

    Returns:
        dict: Access token response in JSON format.
    """

    token_url = "https://api.petfinder.com/v2/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": PETFINDER_API_KEY,
        "client_secret": PETFINDER_API_SECRET
    }

    # response = requests.post(token_url, data=data)
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Error: {response.status_code}", "message": response.text}
