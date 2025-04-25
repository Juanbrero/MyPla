import requests
from app.auth0.config import settings

def get_management_token():
    response = requests.post(f'https://{settings.auth0_domain}/oauth/token', json={
        'client_id': settings.auth0_mgmt_client_id,
        'client_secret': settings.auth0_mgmt_client_secret,
        'audience': settings.auth0_audience,
        'grant_type': 'client_credentials'
    })

    if response.status_code != 200:
        raise Exception(f"Error getting token: {response.text}")

    return response.json()['access_token']