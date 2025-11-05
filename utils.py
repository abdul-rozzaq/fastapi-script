from dataclasses import dataclass
from pydantic import BaseModel
import os


import requests
import httpx


class RequestBody(BaseModel):
    part2: str


@dataclass
class AppState:
    part1: str = None
    part2: str = None
    msg: str = None


def get_ngrok_url():
    api_base = os.getenv("NGROK_API_URL", "http://localhost:4040")

    try:
        response = requests.get(f"{api_base}/api/tunnels", timeout=10)
        tunnels = response.json().get("tunnels", [])

        for tunnel in tunnels:
            if tunnel.get("proto") == "https":
                return tunnel.get("public_url")

    except Exception as e:
        print(f"Ngrok URL olishda xatolik: {e}")

    return None


async def post_request(url: str, json_data: dict):
    try:
        print("POST:", url, json_data)

        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(url, json=json_data)

            response.raise_for_status()
            print("Response:", response.json())

            return response.json()

        return response.json()

    except requests.RequestException as e:
        print(f"POST so'rov yuborishda xatolik: {e}")
        return None


async def get_request(url: str, params: dict):
    try:
        print("GET:", url, params)

        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()

            print("Response:", response.json())

            return response.json()

    except requests.RequestException as e:
        print(f"GET so'rov yuborishda xatolik: {e}")

        return None
