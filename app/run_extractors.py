from app.services.extract_pvgis import extract_irradiance
from app.services.extract_openmeteo import extract_openmeteo
# from app.services.extract_ree import extract_demand_ree  # Uncomment when REE token is available
from app.config import DEFAULT_LOCATION, LOCATIONS

def run_pvgis_extraction():
    """
    Extract solar irradiance data from PVGIS API for all locations.
    """
    print("\n📡 Extracting solar irradiance data from PVGIS for all locations...")
    for city in LOCATIONS:
        extract_irradiance(
            location=city,
            startyear=2005,
            endyear=2020
        )

    # 👉 Uncomment below if you only want the default location:
    # extract_irradiance(location=DEFAULT_LOCATION, startyear=2005, endyear=2020)

def run_openmeteo_extraction():
    """
    Extract hourly weather forecast from Open-Meteo for all locations.
    """
    print("\n🌤️ Extracting weather forecast from Open-Meteo for all locations...")
    for city in LOCATIONS:
        extract_openmeteo(
            location=city,
            startyear=2005,
            endyear=2020
        )

    # 👉 Uncomment below if you only want the default location:
    # extract_openmeteo(location=DEFAULT_LOCATION, startyear=2005, endyear=2020)

# def run_ree_extraction():
#     """
#     Placeholder for future REE demand extraction once token is available.
#     """
#     print("⚡ Extracting electricity demand data from REE...")
#     # extract_demand_ree()

if __name__ == "__main__":
    run_openmeteo_extraction()
    run_pvgis_extraction()
    # run_ree_extraction()  # Enable once ready


# # python -m app.run_extractors


