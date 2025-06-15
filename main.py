from fastapi import FastAPI
import httpx

app = FastAPI()

RAPIDAPI_KEY = "f748dbb612msh392946279a904c6p114238jsndac2cd9fbc7b"
RAPIDAPI_HOST = "weatherapi-com.p.rapidapi.com"
FORECAST_URL = f"https://{RAPIDAPI_HOST}/forecast.json"

@app.get("/")
def root():
    return {"message": "Welcome to the Tashkent 14-day Weather API"}

@app.get("/api/tashkent-weather")
async def get_tashkent_forecast():
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    params = {
        "q": "Tashkent",
        "days": 14
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(FORECAST_URL, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            forecast_days = data["forecast"]["forecastday"]

            # Build output: { "YYYY-MM-DD": "Weather condition" }
            result = {
                day["date"]: day["day"]["condition"]["text"]
                for day in forecast_days
            }

            return result

    except Exception as e:
        return {"error": str(e)}
