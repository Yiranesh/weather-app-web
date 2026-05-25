import os
import urllib.request
import urllib.error
import urllib.parse
import json
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY", "ee2171a0bb8ad35325f608b42c42ba11")

CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

COUNTRY_NAMES = {
    "MY": "Malaysia", "GB": "United Kingdom", "US": "United States",
    "SG": "Singapore", "ID": "Indonesia", "TH": "Thailand",
    "PH": "Philippines", "VN": "Vietnam", "BN": "Brunei",
    "CN": "China", "JP": "Japan", "KR": "South Korea",
    "IN": "India", "AU": "Australia", "NZ": "New Zealand",
    "CA": "Canada", "FR": "France", "DE": "Germany",
    "IT": "Italy", "ES": "Spain", "NL": "Netherlands",
    "BR": "Brazil", "AE": "United Arab Emirates"
}

def get_country_name(code):
    return COUNTRY_NAMES.get(code, code)

def get_weather_emoji(condition):
    condition = condition.lower()
    if "clear" in condition:       return "☀️"
    elif "cloud" in condition:     return "☁️"
    elif "rain" in condition:      return "🌧️"
    elif "storm" in condition or "thunder" in condition: return "⛈️"
    elif "snow" in condition:      return "❄️"
    elif "mist" in condition or "fog" in condition: return "🌫️"
    elif "wind" in condition:      return "💨"
    else:                          return "🌤️"

def fetch_json(url):
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"error": "City not found. Please check the spelling."}
        elif e.code == 401:
            return {"error": "Invalid API key."}
        else:
            return {"error": f"HTTP error: {e.code}"}
    except urllib.error.URLError:
        return {"error": "Unable to connect. Check your internet."}

def get_current_weather(city):
    city_enc = urllib.parse.quote(city)
    url = f"{CURRENT_WEATHER_URL}?q={city_enc}&appid={API_KEY}&units=metric"
    data = fetch_json(url)
    if "error" in data:
        return None, data["error"]
    return {
        "city": data["name"],
        "country": get_country_name(data["sys"]["country"]),
        "temp": round(data["main"]["temp"], 1),
        "feels_like": round(data["main"]["feels_like"], 1),
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"],
        "condition": data["weather"][0]["description"].title(),
        "emoji": get_weather_emoji(data["weather"][0]["description"]),
        "icon": data["weather"][0]["icon"],
    }, None

def get_forecast(city):
    city_enc = urllib.parse.quote(city)
    url = f"{FORECAST_URL}?q={city_enc}&appid={API_KEY}&units=metric&cnt=40"
    data = fetch_json(url)
    if "error" in data:
        return None, data["error"]
    seen = set()
    days = []
    for item in data["list"]:
        date = item["dt_txt"][:10]
        if date not in seen:
            seen.add(date)
            condition = item["weather"][0]["description"].title()
            days.append({
                "date": date,
                "temp": round(item["main"]["temp"], 1),
                "condition": condition,
                "emoji": get_weather_emoji(condition),
                "icon": item["weather"][0]["icon"],
                "humidity": item["main"]["humidity"],
            })
        if len(days) == 5:
            break
    return days, None

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/current", methods=["GET", "POST"])
def current():
    weather, error = None, None
    if request.method == "POST":
        city = request.form.get("city", "").strip()
        if city:
            weather, error = get_current_weather(city)
    return render_template("current.html", weather=weather, error=error)

@app.route("/forecast", methods=["GET", "POST"])
def forecast():
    forecast_data, error = None, None
    city_name = ""
    if request.method == "POST":
        city = request.form.get("city", "").strip()
        if city:
            city_name = city
            forecast_data, error = get_forecast(city)
    return render_template("forecast.html", forecast=forecast_data, error=error, city=city_name)

@app.route("/compare", methods=["GET", "POST"])
def compare():
    results, error = None, None
    if request.method == "POST":
        city1 = request.form.get("city1", "").strip()
        city2 = request.form.get("city2", "").strip()
        if city1 and city2:
            w1, e1 = get_current_weather(city1)
            w2, e2 = get_current_weather(city2)
            if e1 or e2:
                error = e1 or e2
            else:
                diff = abs(w1["temp"] - w2["temp"])
                if w1["temp"] > w2["temp"]:
                    warmer = f"{w1['city']} is warmer by {diff:.1f}°C"
                elif w2["temp"] > w1["temp"]:
                    warmer = f"{w2['city']} is warmer by {diff:.1f}°C"
                else:
                    warmer = "Both cities have the same temperature"
                results = {"city1": w1, "city2": w2, "warmer": warmer}
    return render_template("compare.html", results=results, error=error)

if __name__ == "__main__":
    app.run(debug=True)
