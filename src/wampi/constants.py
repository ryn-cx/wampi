# TODO: Validate
"""Constants."""

from pathlib import Path

WAMPI_PATH = Path(__file__).parent
FILES_PATH = WAMPI_PATH / "_files"

API_DOMAIN = "api.watchmode.com"
BASE_API_URL = f"https://{API_DOMAIN}/v1"

API_KEY_CREDENTIAL = "WATCHMODE_API_KEY"
"""Name the API key is stored under in the keyring or the `.env` file."""
