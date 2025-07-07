import requests
import pandas as pd
from pathlib import Path
from app.config import get_coordinates

def extract_nasa_power(location: str, start: str, end: str):
    print(f"🌍 Fetching NASA POWER data for {location.title()} ({start} to {end})...")
    lat, lon = get_coordinates(location)

    parameters = [
        "ALLSKY_SFC_SW_DWN", "T2M", "RH2M", "WS10M",
        "CLRSKY_SFC_SW_DWN", "T2M_MAX", "T2M_MIN"
    ]

    base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "parameters": ",".join(parameters),
        "start": start,
        "end": end,
        "latitude": lat,
        "longitude": lon,
        "format": "JSON",
        "community": "RE"
    }

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        print(f"❌ Error {response.status_code}: {response.text}")
        return

    json_data = response.json()
    records = json_data.get("properties", {}).get("parameter", {})
    if not records:
        print("⚠️ No data received.")
        return

    df = pd.DataFrame(records).T
    df.index.name = "date"
    df.reset_index(inplace=True)

    output_path = Path("data") / location.lower() / f"nasa_{start[:4]}.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ NASA POWER data saved to {output_path}")

