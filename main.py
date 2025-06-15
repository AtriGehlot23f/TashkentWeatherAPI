from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BBC_LOCATION_API = "https://locator-service.api.bbc.com/locations?search={city}&filter=weather"
BBC_WEATHER_API = "https://weather-broker-cdn.api.bbci.co.uk/en/forecast/rss/3day/{location_id}"

@app.get("/api/tashkent-weather")
async def get_tashkent_weather():
    city = "Tashkent"
    
    try:
        # Get location ID
        async with httpx.AsyncClient() as client:
            response = await client.get(BBC_LOCATION_API.format(city=city))
            response.raise_for_status()
            data = response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch location ID: {e}")

    # Extract location ID
    try:
        location_id = data["response"]["results"][0]["id"]
    except (KeyError, IndexError):
        raise HTTPException(status_code=404, detail="404: Location ID not found")

    # Get weather data
    try:
        weather_url = f"https://weather-broker-cdn.api.bbci.co.uk/en/forecast/api/observe/{location_id}"
        async with httpx.AsyncClient() as client:
            response = await client.get(weather_url)
            response.raise_for_status()
            weather_data = response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch weather data: {e}")

    try:
        forecasts = weather_data["forecasts"]
        result = {}
        for forecast in forecasts:
            date = forecast.get("localDate")
            description = forecast.get("enhancedWeath")
