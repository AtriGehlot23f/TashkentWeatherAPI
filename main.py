from fastapi import FastAPI
import httpx

app = FastAPI()

RAPIDAPI_KEY = "f748dbb612msh392946279a904c6p114238jsndac2cd9fbc7b"
RAPIDAPI_HOST = "weatherapi-com.p.rapidapi.com"
FORECAST_URL = f"https://{RAPIDAPI_HOST}/forecast.json"

@app.get("/")
def root():
    return {"message": "Welcome to Tashkent Weather Forecast API"}

@app.get("/api/tashkent-weather")
async def get_tashkent_forecast():
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    params = {
        "q": "Tashkent",
        "days": 7,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(FORECAST_URL, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            forecast_data = data["forecast"]["forecastday"]

            result = {}
            for day in forecast_data:
                date = day["date"]
                condition = day["day"]["condition"]["text"]
                temp_c = day["day"]["avgtemp_c"]
                result[date] = f"{condition}, {temp_c}°C"

            return result

    except httpx.RequestError as e:
        return {"error": f"Request error: {e}"}
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP error: {e.response.status_code} - {e.response.text}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
