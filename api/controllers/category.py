from typing import Annotated

from dishka.integrations.litestar import FromDishka, inject
from litestar import Controller, MediaType, get, post, status_codes
from litestar.exceptions import ClientException, NotFoundException
from litestar.response import Response
from litestar.params import Body

from api.controllers.exceptions import ConflictException
from api.entities.exceptions import ConflictError, NotFoundError, RemoteClientError, RemoteServerError
from api.entities.responses import CategoryResponse
from api.entities.schemes import CategoryScheme
from api.entities.services import ICategoryServiceChanger, ICategoryServiceSelector


class CategoryController(Controller):
    swagger_tag = "Category"
    path = "/category/"

    @post(tags=[swagger_tag], path="/", response_model=CategoryResponse)
    @inject
    async def create_category(
        self,
        data: Annotated[CategoryScheme, Body()],
        category_service_changer: FromDishka[ICategoryServiceChanger],
    ) -> Response[CategoryResponse]:
        try:
            response = await category_service_changer.create(
                account_id=data.account_id,
                name=data.name,
                sub_name=data.sub_name,
            )
        except ConflictError as err:
            raise ConflictException(detail=err.message) from err
        except (RemoteClientError, RemoteServerError) as err:
            raise ClientException(detail=err.message) from err

        return Response(content=response, status_code=status_codes.HTTP_201_CREATED, media_type=MediaType.JSON)

    @get(tags=[swagger_tag], path="/{accountId:str}/", response_model=CategoryResponse)
    @inject
    async def get_by_account(
        self,
        accountId: str,  # noqa: N803
        category_service_selector: FromDishka[ICategoryServiceSelector],
    ) -> Response[list[CategoryResponse]]:
        try:
            response = await category_service_selector.get_by_account(account_id=accountId)
        except NotFoundError as err:
            raise NotFoundException(detail=err.message) from err
        except (RemoteClientError, RemoteServerError) as err:
            raise ClientException(detail=err.message) from err

        return Response(content=response, status_code=status_codes.HTTP_200_OK, media_type=MediaType.JSON)
