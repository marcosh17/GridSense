import requests
import pandas as pd
from pathlib import Path
from app.config import get_coordinates

def extract_nasa_data(location: str, start_date: str, end_date: str):
    """Download daily data from NASA POWER and save to data/<city>/raw/."""
    print(f"🚀 Fetching NASA POWER data for {location.title()}...")

    lat, lon = get_coordinates(location)
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "start": start_date,
        "end": end_date,
        "latitude": lat,
        "longitude": lon,
        "community": "RE",
        "parameters": ",".join([
            "ALLSKY_SFC_SW_DWN",  # Global horizontal irradiance (kWh/m²/day)
            "T2M", "T2M_MAX", "T2M_MIN",
            "RH2M", "WS10M",
            "CLRSKY_SFC_SW_DWN"
        ]),
        "format": "JSON",
        "user": "anonymous"
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"❌ Error: Status {response.status_code}")
        print("🔎 Response text:", response.text)
        return

    data = response.json()["properties"]["parameter"]
    df = pd.DataFrame(data)
    df = df.T
    df.index.name = "date"
    df.reset_index(inplace=True)

    output_dir = Path("data") / location.lower() / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"nasa_raw_{start_date}_{end_date}.csv"
    df.to_csv(output_path, index=False)

    print(f"✅ NASA data saved to {output_path}")

