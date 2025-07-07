import requests
import pandas as pd
from datetime import date
from pathlib import Path
from app.config import get_coordinates

def get_atmospheric_data(lat, lon, start, end):
    """Fetch atmospheric variables from Open-Meteo."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start,
        "end_date": end,
        "hourly": ",".join([
            "temperature_2m",
            "cloudcover",
            "windspeed_10m",
            "winddirection_10m"
        ]),
        "timezone": "auto"
    }
    response = requests.get("https://api.open-meteo.com/v1/forecast", params=params)
    response.raise_for_status()
    return pd.DataFrame(response.json().get("hourly", {}))

def get_radiation_data(lat, lon, start, end):
    """Placeholder: radiation data currently not available from Open-Meteo forecast endpoint."""
    return pd.DataFrame(columns=["time", "global_radiation", "shortwave_radiation"])

def extract_openmeteo(location: str):
    """Extract and merge weather + placeholder radiation data from Open-Meteo."""
    print(f"🌤️ Fetching weather data from Open-Meteo for {location.title()}...")
    lat, lon = get_coordinates(location)
    start = date.today().isoformat()
    end = start

    try:
        df_weather = get_atmospheric_data(lat, lon, start, end)
        df_radiation = get_radiation_data(lat, lon, start, end)
        df_merged = pd.merge(df_weather, df_radiation, on="time", how="outer")

        output_path = Path("data") / location.lower() / f"openmeteo_{start}.csv"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df_merged.to_csv(output_path, index=False)
        print(f"✅ Weather data saved to {output_path}")
    except requests.exceptions.HTTPError as e:
        print(f"❌ Error fetching data: {e.response.status_code}")
        print("🔎 Response text:", e.response.text)




