from app.services.extract_pvgis import extract_irradiance
from app.services.extract_openmeteo import extract_openmeteo
from app.config import DEFAULT_LOCATION
# from app.services.extract_ree import extract_demand_ree  # Uncomment when REE token is available

def run_pvgis_extraction():
    """
    Extract solar irradiance data from PVGIS API for the configured location and year.
    """
    print(f"📡 Extracting solar irradiance data from PVGIS for {DEFAULT_LOCATION.title()}...")
    from app.config import get_coordinates
    lat, lon = get_coordinates(DEFAULT_LOCATION)

    extract_irradiance(
        lat=lat,
        lon=lon,
        startyear=2020,
        endyear=2020,
        save_path=f"data/pvgis_{DEFAULT_LOCATION}_2020.csv"
    )

def run_openmeteo_extraction():
    """
    Extract hourly weather forecast from Open-Meteo for the configured location.
    """
    extract_openmeteo(location=DEFAULT_LOCATION)

def run_ree_extraction():
    """
    Placeholder for future REE demand extraction once token is available.
    """
    print("⚡ Extracting electricity demand data from REE...")
    # extract_demand_ree()

if __name__ == "__main__":
    run_pvgis_extraction()
    run_openmeteo_extraction()
    # run_ree_extraction()  # Enable once ready

# python -m app.run_extractors

