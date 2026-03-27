from dishka import AsyncContainer, make_async_container
from dishka.integrations import litestar as litestar_integration
from dynaconf import Dynaconf
from litestar import Litestar
from litestar.openapi import OpenAPIConfig

from api import __about__
from api.config import settings
from api.controllers.routes import route_handlers
from api.ioc import AppProvider


def get_litestar_app(container: AsyncContainer) -> Litestar:
    # TODO: Local Swagger API: http://127.0.0.1:8000/schema/swagger#/
    app = Litestar(
        route_handlers=route_handlers,
        debug=settings.DEBUG,
        openapi_config=OpenAPIConfig(
            title="Finance API",
            description="WEB API of finances",
            version=__about__.version,
        ),
    )
    litestar_integration.setup_dishka(container, app)

    return app


def get_app() -> Litestar:
    container = make_async_container(AppProvider(), context={Dynaconf: settings})

    litestar_app = get_litestar_app(container=container)

    return litestar_app
