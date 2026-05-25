# 🌤 Weather App — Web Version
**by Yiranesh** | Built with Flask + OpenWeatherMap API

A full-featured weather web app with current conditions, 5-day forecasts, and city comparisons.

---

## Features
- 🌡️ **Current Weather** — temperature, humidity, wind, feels-like
- 📅 **5-Day Forecast** — daily outlook with icons
- ⚖️ **City Comparison** — side-by-side weather for two cities

## Tech Stack
- **Backend:** Python + Flask
- **API:** OpenWeatherMap
- **Frontend:** Jinja2 templates + CSS

---

## Run Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python app.py

# 3. Open in browser
http://127.0.0.1:5000
```

## Deploy to Render (Free)

1. Push this folder to a GitHub repo
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your repo and set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
4. Add Environment Variable:
   - `API_KEY` → your OpenWeatherMap API key
5. Click Deploy ✅
