from enum import Enum
from pathlib import Path
from tempfile import gettempdir
from typing import Optional

from pydantic import BaseSettings

from src import __version__

TEMP_DIR = Path(gettempdir())


class LogLevel(str, Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class CommonSettings(BaseSettings):
    """Common settings."""

    APP_NAME: str = "FHIRSARTER"
    APP_VERSION: str = __version__
    # Current environment
    ENVIRONMENT: str = "dev"
    # Logging Level
    LOG_LEVEL: LogLevel = LogLevel.DEBUG
    # This variable is used to define
    # multiproc_dir. It's required for [uvi|guni]corn projects.
    PROMETHEUS_DIR: Path = TEMP_DIR / "prom"
    OPENTELEMETRY_ENDPOINT: Optional[str] = None

    

    


class ServerSettings(BaseSettings):
    """Server settings."""

    # Host app 
    SERVER_HOST: str = "127.0.0.1"
    # app Port
    SERVER_PORT: int = 5000
  
    # quantity of workers for uvicorn
    SERVER_WORKERS_COUNT: int = 1
    # Enable uvicorn reloading
    SERVER_RELOAD: bool = True

    TOPIC_NAME : str =  None

    API_VERSION="/api/v1/patient"


class Settings(CommonSettings, ServerSettings):
    """Application settings."""
    API_VERSION: str = None
    #REDIS CONFIGURATION
    #Host app 
    REDIS_HOST : str = None
    #Redis port
    REDIS_PORT : str = None
    #MONGODB CONFIGURATION
    MONGO_URI : str = None
   
    MONGO_COLLECTION : str = None

    

    API_VERSION="/api/v1/patient"
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
