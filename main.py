from fastapi import FastAPI
import httpx
import os

app = FastAPI()

RAPIDAPI_KEY = "f748dbb612msh392946279a904c6p114238jsndac2cd9fbc7b"
RAPIDAPI_HOST = "weatherapi-com.p.rapidapi.com"
BASE_URL = f"https://{RAPIDAPI_HOST}/current.json"

@app.get("/")
def root():
    return {"message": "Welcome to Tashkent Weather API"}

@app.get("/api/tashkent-weather")
async def get_tashkent_weather():
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    params = {
        "q": "Tashkent"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(BASE_URL, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            current = data["current"]
            location = data["location"]

            return {
                "location": location["name"],
                "country": location["country"],
                "temperature_c": current["temp_c"],
                "condition": current["condition"]["text"],
                "wind_kph": current["wind_kph"],
                "humidity": current["humidity"],
                "localtime": location["localtime"]
            }

    except httpx.RequestError as e:
        return {"error": f"Request error: {e}"}
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP error: {e.response.status_code} - {e.response.text}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
