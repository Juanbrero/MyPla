import requests
from app.auth0.config import settings

def get_management_token():
    payload = {
        "grant_type": "client_credentials",
        "client_id": settings.auth0_mgmt_client_id,
        "client_secret": settings.auth0_mgmt_client_secret,
        "audience": f"https://{settings.auth0_domain}/api/v2/"
    }

    response = requests.post(f"https://{settings.auth0_domain}/oauth/token", json=payload)
    if response.status_code != 200:
        raise Exception(f"Error al obtener token: {response.text}")

    return response.json()["access_token"]
