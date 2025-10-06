import requests
from .decorators import mcp
from mcp.config import EXCHANGE_RATE_API_KEY

@mcp.tool("weather_forecast")
def weather_forecast(city: str):
    try:
        geo_res = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1}
        ).json()

        if not geo_res.get("results"):
            return {"error": f"City '{city}' not found."}

        lat = geo_res["results"][0]["latitude"]
        lon = geo_res["results"][0]["longitude"]

        weather_res = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": lat, "longitude": lon, "current_weather": True}
        ).json()

        return {
            "city": city,
            "latitude": lat,
            "longitude": lon,
            "current_weather": weather_res.get("current_weather", {})
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool("usd_to_inr")
def usd_to_inr():
    try:
        if not EXCHANGE_RATE_API_KEY:
            return {"error": "Missing EXCHANGE_RATE_API_KEY"}

        res = requests.get(
            f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/USD"
        ).json()

        if res.get("result") != "success":
            return {"error": "Failed to fetch exchange rates"}

        rate = res["conversion_rates"].get("INR")
        return {"USD_INR": rate}
    except Exception as e:
        return {"error": str(e)}
    

GOLD_PRICE_API_URL = "https://data-asg.goldprice.org/dbXRates/USD"

@mcp.tool("gold_price")
def gold_price():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(GOLD_PRICE_API_URL, headers=headers, timeout=5)

        if resp.status_code != 200:
            return {"error": f"Gold price API request failed with status {resp.status_code}"}

        data = resp.json()
        if "items" not in data or not data["items"]:
            return {"error": "No gold price data available."}

        gold_usd_per_ounce = data["items"][0].get("xauPrice")
        if not gold_usd_per_ounce:
            return {"error": "Gold price not found in API response."}

        # Convert ounce → gram
        gold_usd_per_gram = gold_usd_per_ounce / 31.1035

        return {
            "USD_per_gram": round(gold_usd_per_gram, 2),
            "source": "GoldPrice API",
            "timestamp": data.get("timestamp", "")
        }

    except Exception as e:
        return {"error": str(e)}


@mcp.resource("api_endpoints")
def get_api_endpoints():
    """
    Resource to store and provide API endpoints used in the application.
    """
    return {
        "weather": {
            "geocoding": "https://geocoding-api.open-meteo.com/v1/search",
            "forecast": "https://api.open-meteo.com/v1/forecast"
        },
        "exchange_rate": f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/USD",
        "gold_price": GOLD_PRICE_API_URL
    }

@mcp.prompt("weather_query")
def generate_weather_query(city: str):
    """
    Generates a structured prompt for weather-related queries.
    """
    return {
        "system_message": "You are a weather information assistant.",
        "prompt_template": f"Please provide the current weather information for {city}.",
        "parameters": {
            "city": city,
            "required_fields": ["temperature", "wind_speed", "weather_condition"]
        }
    }

@mcp.prompt("currency_query")
def generate_currency_query():
    """
    Generates a structured prompt for currency conversion queries.
    """
    return {
        "system_message": "You are a currency conversion assistant.",
        "prompt_template": "Please provide the current USD to INR exchange rate.",
        "parameters": {
            "currencies": ["USD", "INR"],
            "required_fields": ["exchange_rate", "last_updated"]
        }
    }

@mcp.prompt("gold_price_query")
def generate_gold_query():
    """
    Generates a structured prompt for gold price queries.
    """
    return {
        "system_message": "You are a precious metals price information assistant.",
        "prompt_template": "Please provide the current gold price per gram in USD.",
        "parameters": {
            "metal": "gold",
            "unit": "gram",
            "currency": "USD",
            "required_fields": ["price_per_gram", "price_per_ounce", "timestamp", "source"]
        }
    }