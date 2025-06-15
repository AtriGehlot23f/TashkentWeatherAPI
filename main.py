from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

BBC_LOCATOR_URL = "https://locator-service.api.bbc.com/locations?search={}"
BBC_WEATHER_URL = "https://weather-broker-cdn.api.bbci.co.uk/en/forecast/aggregated/{}"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

@app.get("/api/tashkent-weather")
async def get_weather():
    city = "Tashkent"

    # Step 1: Get location ID
    try:
        async with httpx.AsyncClient() as client:
            locator_resp = await client.get(BBC_LOCATOR_URL.format(city), headers=HEADERS)
            locator_resp.raise_for_status()
            data = locator_resp.json()
            print("BBC Locator API response:", data)
    except Exception as e:
        print("Failed to fetch location ID:", str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch location ID")

    try:
        location_id = data["data"][0]["id"]
        print("Location ID:", location_id)
    except (KeyError, IndexError) as e:
        print("Error extracting location ID:", str(e))
        raise HTTPException(status_code=404, detail="Location ID not found")

    # Step 2: Get weather data
    weather_api_url = BBC_WEATHER_URL.format(location_id)
    try:
        async with httpx.AsyncClient() as client:
            weather_resp = await client.get(weather_api_url, headers=HEADERS)
            weather_resp.raise_for_status()
            forecast_data = weather_resp.json()
            print("BBC Weather API response:", forecast_data)
    except Exception as e:
        print("Failed to fetch weather data:", str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch weather data")

    try:
        forecasts = forecast_data["forecasts"]
        result = {
            entry["date"]: entry["summary"]["description"]
            for entry in forecasts
        }
        return result
    except Exception as e:
        print("Failed to parse forecast:", str(e))
        raise HTTPException(status_code=500, detail="Failed to parse forecast")
