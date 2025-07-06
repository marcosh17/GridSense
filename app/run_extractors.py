from app.services.extract_pvgis import extract_irradiance
from app.config import LATITUDE, LONGITUDE, DEFAULT_LOCATION
# from services.extract_ree import extract_demand_ree  # Uncomment when REE token is available

def run_pvgis_extraction():
    """
    Extract solar irradiance data from PVGIS API for the configured location and year.
    """
    print(f"📡 Extracting solar irradiance data from PVGIS for {DEFAULT_LOCATION.title()}...")
    extract_irradiance(
        lat=LATITUDE,
        lon=LONGITUDE,
        startyear=2020,
        endyear=2020,
        save_path=f"data/pvgis_{DEFAULT_LOCATION}_2020.csv"
    )

def run_ree_extraction():
    """
    Placeholder for future REE demand extraction once token is available.
    """
    print("⚡ Extracting electricity demand data from REE...")
    # extract_demand_ree()

if __name__ == "__main__":
    run_pvgis_extraction()
    # run_ree_extraction()  # Enable once ready


# python -m app.run_extractors
