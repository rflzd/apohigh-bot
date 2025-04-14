# services/highlightly.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

headers = {
    "x-rapidapi-key": RAPIDAPI_KEY
}

def get_leagues(limit=10, offset=0, countryCode=None, season=None):
    params = {
        "limit": limit,
        "offset": offset
    }

    if countryCode:
        params["countryCode"] = countryCode
    if season:
        params["season"] = season

    url = f"{API_BASE_URL}/leagues"
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()
