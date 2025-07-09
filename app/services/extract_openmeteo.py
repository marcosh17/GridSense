import requests
import pandas as pd
import time
from datetime import date
from pathlib import Path
from app.config import get_coordinates

def get_atmospheric_data(lat, lon, start, end):
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
    response = requests.get("https://archive-api.open-meteo.com/v1/archive", params=params)
    response.raise_for_status()
    return pd.DataFrame(response.json().get("hourly", {}))

def get_radiation_data(lat, lon, start, end):
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start,
        "end_date": end,
        "hourly": ",".join([
            "shortwave_radiation",
            "direct_radiation",
            "diffuse_radiation",
            "cloud_cover"
        ]),
        "timezone": "auto"
    }
    response = requests.get("https://archive-api.open-meteo.com/v1/archive", params=params)
    response.raise_for_status()
    return pd.DataFrame(response.json().get("hourly", {}))

def extract_openmeteo(location: str, startyear: int, endyear: int):
    """
    Extract and save hourly weather and radiation data from Open-Meteo for a given location and year range.
    """
    lat, lon = get_coordinates(location)
    all_data = []

    for year in range(startyear, endyear + 1):
        print(f"📅 Fetching Open-Meteo data for {location.title()} - {year}...")
        start = f"{year}-01-01"
        end = f"{year}-12-31"

        try:
            df_weather = get_atmospheric_data(lat, lon, start, end)
            df_radiation = get_radiation_data(lat, lon, start, end)
            df = pd.merge(df_weather, df_radiation, on="time", how="outer")
            df["time"] = pd.to_datetime(df["time"])
            df["city"] = location.lower()
            all_data.append(df)
        except requests.exceptions.HTTPError as e:
            print(f"❌ Error fetching data for {location.title()} ({year}): {e.response.status_code}")
            print("🔎 Response text:", e.response.text)
        finally:
            time.sleep(2)  # Espera para evitar el rate limit

    if not all_data:
        print(f"⚠️ No data retrieved for {location.title()}")
        return

    full_df = pd.concat(all_data, ignore_index=True)

    output_dir = Path("data") / location.lower() / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"openmeteo_{location.lower()}_{startyear}_{endyear}.csv"
    full_df.to_csv(output_path, index=False)
    print(f"✅ Open-Meteo data saved to {output_path}")


