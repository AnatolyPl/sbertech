import os

from .app import get_config, AppConfiguration
from .logger import get_logger

environment = os.getenv("ENV_NAME", "local")
APP_NAME = "hecate"

app_config = get_config()
