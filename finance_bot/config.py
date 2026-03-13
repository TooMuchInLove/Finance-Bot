from os import getcwd, mkdir
from sys import stdout as sys_std_out
from dataclasses import dataclass

from loguru import logger
from dynaconf import Dynaconf

logger_config_map = {
    "handlers": [
        {
            "sink": sys_std_out,
            "level": "DEBUG",
            "colorize": True,
            "backtrace": True,
            "diagnose": True,
        },
    ]
}
logger.configure(**logger_config_map)

settings = Dynaconf(
    envvar_prefix="TFB",
    load_dotenv=True,
    env_switcher="TFB_MODE",
)

project_path = f"{'/'.join(getcwd().split('/')[:-1])}/{settings.PROJECT_NAME}"
database_path = f"{project_path}/{settings.DATABASE_DIRECTORY_NAME}"

try:
    mkdir(database_path)
except FileExistsError:
    pass


@dataclass(slots=True, frozen=True)
class DataBaseSettings:
    name = settings.DATABASE_NAME
    path = database_path

    def dsn(self) -> str:
        return f"{self.path}/{self.name}.db"


db_settings = DataBaseSettings()
