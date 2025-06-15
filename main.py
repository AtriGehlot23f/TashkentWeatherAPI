from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

def get_location_id(city: str) -> str:
    url = f"https://weather-broker.api.bbci.co.uk/locations/v4/search?query={city}&lang=en"
    res = requests.get(url)
    if res.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch location ID")
    data = res.json()
    try:
        return data[0]['id']
    except (KeyError, IndexError):
        raise HTTPException(status_code=404, detail="Location ID not found")

def get_forecast(location_id: str) -> dict:
    url = f"https://weather-broker.api.bbci.co.uk/en/forecast/aggregated/{location_id}"
    res = requests.get(url)
    if res.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch forecast")
    data = res.json()
    try:
        return {
            day["localDate"]: day["enhancedWeatherDescription"]
            for day in data["forecasts"]
        }
    except KeyError:
        raise HTTPException(status_code=500, detail="Forecast data missing")

@app.get("/api/tashkent-weather")
async def tashkent_weather():
    city = "Tashkent"
    location_id = get_location_id(city)
    forecast = get_forecast(location_id)
    return forecast
