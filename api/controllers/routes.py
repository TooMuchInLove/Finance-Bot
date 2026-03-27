from litestar import Router

from api.controllers.account import AccountController
from api.controllers.category import CategoryController
from api.controllers.healthcheck import healthcheck

routes_version_v1 = [
    healthcheck,
    AccountController,
    CategoryController,
]

api = "api"
version_v1 = "v1"

route_handlers = [
    Router(path="/", route_handlers=[healthcheck]),
    Router(path=f"/{api}/{version_v1}/", route_handlers=routes_version_v1),
]
