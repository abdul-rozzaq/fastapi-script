from pydantic import BaseModel

import requests


class RequestBody(BaseModel):
    part2: str


def get_ngrok_url():
    try:
        response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
        tunnels = response.json().get("tunnels", [])
        for tunnel in tunnels:
            if tunnel.get("proto") == "https":
                return tunnel.get("public_url")

    except Exception as e:
        print(f"Ngrok URL olishda xatolik: {e}")
    return None


def post_request(url: str, json_data: dict):
    try:
        print("POST:", url, json_data)

        response = requests.post(url, json=json_data)
        response.raise_for_status()

        print("Response:", response.json())

        return response.json()
    except requests.RequestException as e:
        print(f"POST so'rov yuborishda xatolik: {e}")
        return None


def get_request(url: str, params: dict):
    try:
        print("GET:", url, params)
        response = requests.get(url, params=params)
        response.raise_for_status()
        print("Response:", response.json())
        return response.json()
    except requests.RequestException as e:
        print(f"GET so'rov yuborishda xatolik: {e}")
        return None
