from utils.config import API_BASE_URL, API_KEY
import requests

headers = {
    "x-rapidapi-key": API_KEY
}

def get_leagues_by_country(country_name):
    url = f"{API_BASE_URL}/leagues?countryName={country_name}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("data", [])  # bəzi cavablar {"data": [...]} formatında ola bilər
    else:
        print("API error:", response.status_code)
        return []


def get_matches_by_league_name(league_name, mode):
    url = f"{API_BASE_URL}/matches?leagueName={league_name}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        matches = response.json().get("data", [])

        if mode == "live":
            return [m for m in matches if m["state"].lower() not in ["not started", "finished"]]
        elif mode == "prematch":
            return [m for m in matches if m["state"].lower() == "not started"]
        return matches
    else:
        print("API error (matches):", response.status_code)
        return []
       
def get_match_details(match_id: int):
    url = f"{API_BASE_URL}/matches/{match_id}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"API xətası: {response.status_code}")
        return None
