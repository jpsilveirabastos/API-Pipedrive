from dotenv import load_dotenv, find_dotenv
import os
import envkey
from pathlib import Path

# Uploading credentials from .env
dotenv_path = Path('.env')
load_dotenv(find_dotenv(raise_error_if_not_found=False))

def get_environment(name: str) -> str:
    if (os.environ.get('ENVKEY')):
        return envkey.get(name)

    return os.get_environment(name)

# Access to Pipedrive
API_TOKEN = os.getenv('API_TOKEN')
USER_WEBHOOK = os.getenv('USER_WEBHOOK')
PASSWORD_WEBHOOK = os.getenv('PASSWORD_WEBHOOK')

# Access to Postgres
DBNAME = os.getenv('DBNAME')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
