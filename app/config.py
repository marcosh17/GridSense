from dotenv import load_dotenv
import os
from data.locations import LOCATIONS  

load_dotenv()

# Token API REE
ESIOS_TOKEN = os.getenv("ESIOS_TOKEN")

if not ESIOS_TOKEN:
    raise EnvironmentError("ESIOS_TOKEN is not set in the .env file")

DEFAULT_LOCATION = "madrid"
LATITUDE = LOCATIONS[DEFAULT_LOCATION]["lat"]
LONGITUDE = LOCATIONS[DEFAULT_LOCATION]["lon"]
