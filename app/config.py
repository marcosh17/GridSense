from dotenv import load_dotenv
import os
from data.locations import LOCATIONS  

load_dotenv()

# Token API REE
ESIOS_TOKEN = os.getenv("ESIOS_TOKEN")

if not ESIOS_TOKEN:
    raise EnvironmentError("ESIOS_TOKEN is not set in the .env file")

DEFAULT_LOCATION = "madrid"

def get_coordinates(city: str):
    city = city.lower()
    if city not in LOCATIONS:
        raise ValueError(f"City '{city}' not found in locations dictionary.")
    return LOCATIONS[city]["lat"], LOCATIONS[city]["lon"]
