import requests
import pandas as pd

def extract_irradiance(lat, lon, startyear=2023, endyear=2023, save_path="data/pvgis_madrid.csv"):
    url = "https://re.jrc.ec.europa.eu/api/v5_2/seriescalc"
    params = {
        "lat": lat,
        "lon": lon,
        "startyear": startyear,
        "endyear": endyear,
        "outputformat": "json",
        "angle": 35,
        "aspect": 0,      # 0 = south-facing
        "pvcalculation": 0,  # Use just irradiance, no simulation
    }

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

    df.to_csv(save_path, index=False)
    print(f"✅ Irradiance data successfully saved to {save_path}")
