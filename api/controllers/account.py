from typing import Annotated

from dishka.integrations.litestar import FromDishka, inject
from litestar import Controller, MediaType, get, post, status_codes
from litestar.exceptions import ClientException, NotFoundException
from litestar.response import Response
from litestar.params import Body

from api.controllers.exceptions import ConflictException
from api.entities.exceptions import ConflictError, NotFoundError, RemoteClientError, RemoteServerError
from api.entities.responses import AccountResponse
from api.entities.schemes import AccountScheme
from api.entities.services import IAccountServiceChanger, IAccountServiceSelector


class AccountController(Controller):
    swagger_tag = "Account"
    path = "/account/"

    @post(tags=[swagger_tag], path="/", response_model=AccountResponse)
    @inject
    async def create_account(
        self,
        data: Annotated[AccountScheme, Body()],
        account_service_changer: FromDishka[IAccountServiceChanger],
    ) -> Response[AccountResponse]:
        try:
            response = await account_service_changer.create(
                telegram_user_id=data.telegram_user_id,
                telegram_username=data.telegram_username,
            )
        except ConflictError as err:
            raise ConflictException(detail=err.message) from err
        except (RemoteClientError, RemoteServerError) as err:
            raise ClientException(detail=err.message) from err

        return Response(content=response, status_code=status_codes.HTTP_201_CREATED, media_type=MediaType.JSON)

    @get(tags=[swagger_tag], path="/{telegramUserId:int}/", response_model=AccountResponse)
    @inject
    async def get_account_by_telegram_user_id(
        self,
        telegramUserId: int,  # noqa: N803
        account_service_selector: FromDishka[IAccountServiceSelector],
    ) -> Response[AccountResponse]:
        try:
            response = await account_service_selector.get_by_telegram_user_id(telegram_user_id=telegramUserId)
        except NotFoundError as err:
            raise NotFoundException(detail=err.message) from err
        except (RemoteClientError, RemoteServerError) as err:
            raise ClientException(detail=err.message) from err

        return Response(content=response, status_code=status_codes.HTTP_200_OK, media_type=MediaType.JSON)
