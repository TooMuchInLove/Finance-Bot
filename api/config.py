from logging import config

from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="FINANCE_API",
    load_dotenv=True,
    env_switcher="FINANCE_API_MODE",
)
config.dictConfig(settings.get("LOGGING") or {"version": 1})
