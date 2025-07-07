from app.services.extract_pvgis import extract_irradiance
from app.services.extract_openmeteo import extract_openmeteo
from app.services.extract_nasa_power import extract_nasa_data
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
        location=DEFAULT_LOCATION,
        startyear=2020,
        endyear=2020
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
    
def run_nasa_extraction():
    """
    Extract historical irradiance and weather data from NASA POWER API.
    """
    extract_nasa_data(
        location=DEFAULT_LOCATION,
        start_date="20200101",
        end_date="20201231"
    )


if __name__ == "__main__":
    run_pvgis_extraction()
    run_openmeteo_extraction()
    run_nasa_extraction()
    # run_ree_extraction()  # Enable once ready

# python -m app.run_extractors

