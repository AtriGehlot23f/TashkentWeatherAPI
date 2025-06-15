from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import re
import xml.etree.ElementTree as ET

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET"], allow_headers=["*"])

def get_location_id(city: str) -> str:
    url = f"https://www.bbc.com/weather/search?q={city}"
    res = requests.get(url)
    if res.status_code != 200:
        raise HTTPException(status_code=404, detail="City search failed")
    m = re.search(r"bbc\.com/weather/(\d+)", res.url)
    if not m:
        raise HTTPException(status_code=404, detail="Location ID not found")
    return m.group(1)

def get_forecast_xml(location_id: str) -> dict:
    feed_url = f"https://weather-broker-cdn.api.bbci.co.uk/en/forecast/rss/3day/{location_id}"
    res = requests.get(feed_url)
    if res.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch forecast")
    # Parse RSS XML for localDate and description
    root = ET.fromstring(res.content)
    forecast = {}
    for item in root.findall(".//item"):
        title = item.findtext("title")  # includes date and summary
        desc = item.findtext("description")
        # Title might be like "Wed, 16 Jun 2025 – Sunny"
        date = title.split("–")[0].strip()
        forecast[date] = desc
    return forecast

@app.get("/api/tashkent-weather")
async def tashkent_weather():
    loc = get_location_id("Tashkent")
    data = get_forecast_xml(loc)
    return data
