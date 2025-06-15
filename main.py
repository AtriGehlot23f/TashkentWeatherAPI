from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

BBC_LOCATOR_URL = "https://locator-service.api.bbc.com/locations?search={}"
BBC_WEATHER_URL = "https://weather-broker-cdn.api.bbci.co.uk/en/forecast/rss/3day/{}"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

@app.get("/api/tashkent-weather")
async def get_weather():
    city = "Tashkent"

    # Step 1: Get location ID
    async with httpx.AsyncClient() as client:
        try:
            locator_resp = await client.get(BBC_LOCATOR_URL.format(city), headers=HEADERS)
            data = locator_resp.json()
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to fetch location ID")

    try:
        location_id = data["data"][0]["id"]
    except (KeyError, IndexError):
        raise HTTPException(status_code=404, detail="404: Location ID not found")

    # Step 2: Get weather data (JSON format version)
    weather_api_url = f"https://weather-broker-cdn.api.bbci.co.uk/en/forecast/aggregated/{location_id}"
    async with httpx.AsyncClient() as client:
        try:
            weather_resp = await client.get(weather_api_url, headers=HEADERS)
            forecast_data = weather_resp.json()
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to fetch weather data")

    try:
        forecasts = forecast_data["forecasts"]
        result = {
            entry["date"]: entry["summary"]["description"]
            for entry in forecasts
        }
        return result
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to parse forecast")
