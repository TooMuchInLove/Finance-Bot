from litestar.exceptions import ClientException
from litestar.status_codes import HTTP_409_CONFLICT


class ConflictException(ClientException):
    """Request has been processed, and the resource already exists."""

    status_code = HTTP_409_CONFLICT
