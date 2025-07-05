from dotenv import load_dotenv
import os

load_dotenv()  

ESIOS_TOKEN = os.getenv("ESIOS_TOKEN")

if not ESIOS_TOKEN:
    raise EnvironmentError("ESIOS_TOKEN is not set in the .env file")
