# settings.py
from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path, verbose=True)

SENDY_USERNAME = os.getenv('SENDY_USERNAME')
SENDY_API_KEY = os.getenv('SENDY_API_KEY')
