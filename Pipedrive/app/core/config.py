from dotenv import load_dotenv, find_dotenv
import os
import envkey
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(find_dotenv(raise_error_if_not_found=False))

def get_environment(name: str) -> str:
    if (os.environ.get('ENVKEY')):
        return envkey.get(name)

    return os.get_environment(name)

# Acesso para o Pipedrive
API_TOKEN = os.getenv('API_TOKEN')
USER_WEBHOOK = get_environment('USER_WEBHOOK')
PASSWORD_WEBHOOK = get_environment('PASSWORD_WEBHOOK')

# Acesso para o Postgres
DBNAME = os.getenv('DBNAME')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
