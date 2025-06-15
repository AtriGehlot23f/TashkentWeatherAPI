from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

BBC_LOCATOR_URL = "https://weather-broker-cdn.api.bbci.co.uk/en/observation/search/search"
BBC_FORECAST_URL = "https://weather-broker-cdn.api.bbci.co.uk/en/forecast/aggregated/{}"

@app.get("/api/tashkent-weather")
async def get_tashkent_weather():
    city = "tashkent"
    
    try:
        # Step 1: Get location ID
        locator_resp = httpx.get(BBC_LOCATOR_URL, params={"q": city})
        data = locator_resp.json()
        if not data.get("results"):
            raise HTTPException(status_code=404, detail="Location ID not found")
        location_id = data["results"][0]["id"]

        # Step 2: Get weather forecast
        forecast_resp = httpx.get(BBC_FORECAST_URL.format(location_id))
        forecast_data = forecast_resp.json()
        forecasts = forecast_data.get("forecasts", [])

        if not forecasts:
            raise HTTPException(status_code=404, detail="No forecast data found")

        # Step 3: Format result
        output = {
            day["localDate"]: day["enhancedWeatherDescription"]
            for day in forecasts
        }
        return output

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
