import requests
import pandas as pd
from pathlib import Path
from app.config import get_coordinates

def extract_irradiance(location, startyear=2023, endyear=2023):
    """Extract hourly global irradiance from PVGIS and save to data/<city>/raw/."""
    print(f"📡 Extracting solar irradiance data from PVGIS for {location.title()}...")

    lat, lon = get_coordinates(location)
    url = "https://re.jrc.ec.europa.eu/api/v5_2/seriescalc"
    params = {
        "lat": lat,
        "lon": lon,
        "startyear": startyear,
        "endyear": endyear,
        "outputformat": "json",
        "angle": 35,
        "aspect": 0,
        "pvcalculation": 0
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"❌ Error: Status {response.status_code}")
        print("🔎 Response text:", response.text)
        return

    data = response.json()["outputs"]["hourly"]
    df = pd.DataFrame(data)
    df["time"] = pd.to_datetime(df["time"], format="%Y%m%d:%H%M")
    df = df[["time", "G(i)"]].rename(columns={"G(i)": "global_irradiance_W_m2"})

    output_dir = Path("data") / location.lower() / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"pvgis_{location.lower()}_{startyear}.csv"
    df.to_csv(output_path, index=False)

    print(f"✅ Irradiance data saved to {output_path}")
