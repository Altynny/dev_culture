import requests

BASE_URL = "http://localhost:8000"

def get_users():
    response = requests.get(f"{BASE_URL}/users/")
    if response.ok:
        return response
    else:
        return None

def get_files():
    response = requests.get(f"{BASE_URL}/users/1/files/")
    if response.ok:
        return response
    else:
        return None
