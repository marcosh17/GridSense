import requests
import pandas as pd
from pathlib import Path
from app.config import get_coordinates

def extract_irradiance(location, startyear=2023, endyear=2023):
    lat, lon = get_coordinates(location)

    url = "https://re.jrc.ec.europa.eu/api/v5_2/seriescalc"
    params = {
        "lat": lat,
        "lon": lon,
        "startyear": startyear,
        "endyear": endyear,
        "outputformat": "json",
        "angle": 35,
        "aspect": 0,        # 0 = south-facing
        "pvcalculation": 0  # Only irradiance, no PV simulation
    }

    print(f"📡 Requesting PVGIS irradiance data for {location.title()} ({startyear})...")
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"❌ Error: Unable to fetch data. Status code {response.status_code}")
        print("🔎 Response text:", response.text)
        return

    data = response.json()
    hourly_data = data["outputs"]["hourly"]

    df = pd.DataFrame(hourly_data)
    df["time"] = pd.to_datetime(df["time"], format="%Y%m%d:%H%M")
    df = df[["time", "G(i)"]].rename(columns={"G(i)": "global_irradiance_W_m2"})

    output_path = Path("data") / location.lower() / f"pvgis_{startyear}.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Irradiance data successfully saved to {output_path}")
