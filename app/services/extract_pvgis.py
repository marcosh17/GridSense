# import requests
# import pandas as pd
# from pathlib import Path
# from app.config import get_coordinates

# def extract_irradiance(location: str, startyear=2005, endyear=2025):
#     print(f"📡 Extracting solar irradiance data from PVGIS for {location.title()} ({startyear}–{endyear})...")
    
#     lat, lon = get_coordinates(location)
#     all_data = []

#     for year in range(startyear, endyear + 1):
#         url = "https://re.jrc.ec.europa.eu/api/v5_2/seriescalc"
#         params = {
#             "lat": lat,
#             "lon": lon,
#             "startyear": year,
#             "endyear": year,
#             "outputformat": "json",
#             "angle": 35,
#             "aspect": 0,
#             "pvcalculation": 0
#         }

#         response = requests.get(url, params=params)

#         if response.status_code != 200:
#             print(f"❌ Error fetching year {year}: Status {response.status_code}")
#             continue

#         try:
#             data = response.json()["outputs"]["hourly"]
#             df = pd.DataFrame(data)
#             df["time"] = pd.to_datetime(df["time"], format="%Y%m%d:%H%M")
#             df["year"] = year
#             all_data.append(df[["time", "G(i)"]])
#             print(f"✅ Year {year} loaded successfully.")
#         except Exception as e:
#             print(f"⚠️ Could not process data for year {year}: {e}")

#     if not all_data:
#         print("❌ No data extracted.")
#         return

#     df_final = pd.concat(all_data)
#     df_final.rename(columns={"G(i)": "global_irradiance_W_m2"}, inplace=True)

#     output_dir = Path("data") / location.lower() / "raw"
#     output_dir.mkdir(parents=True, exist_ok=True)
#     output_path = output_dir / f"pvgis_{location.lower()}_{startyear}_{endyear}.csv"

#     df_final.to_csv(output_path, index=False)
#     print(f"✅ Irradiance data saved to {output_path}")

import requests
import pandas as pd
from pathlib import Path
from app.config import get_coordinates

def extract_irradiance(location: str, startyear: int, endyear: int):
    """
    Extract and save hourly solar irradiance data from PVGIS for a given location and year range.
    """
    lat, lon = get_coordinates(location)
    all_data = []

    for year in range(startyear, endyear + 1):
        print(f"📅 Fetching PVGIS data for {location.title()} - {year}...")
        url = "https://re.jrc.ec.europa.eu/api/v5_2/seriescalc"
        params = {
            "lat": lat,
            "lon": lon,
            "startyear": year,
            "endyear": year,
            "outputformat": "json",
            "angle": 35,
            "aspect": 0,
            "pvcalculation": 0,
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"❌ Failed to retrieve data for {location.title()} ({year}): {response.status_code}")
            continue

        hourly_data = response.json()["outputs"]["hourly"]
        df = pd.DataFrame(hourly_data)
        df["time"] = pd.to_datetime(df["time"], format="%Y%m%d:%H%M")
        df = df[["time", "G(i)"]].rename(columns={"G(i)": "global_irradiance_W_m2"})
        df["city"] = location.lower()
        all_data.append(df)

    if not all_data:
        print(f"⚠️ No data retrieved for {location.title()}")
        return

    full_df = pd.concat(all_data, ignore_index=True)

    output_dir = Path("data") / location.lower() / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"pvgis_{location.lower()}_{startyear}_{endyear}.csv"
    full_df.to_csv(output_path, index=False)
    print(f"✅ Irradiance data saved to {output_path}")

