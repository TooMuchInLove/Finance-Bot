from litestar import MediaType, Response, get, status_codes


@get(tags=["Default"], path="/healthcheck/")
async def healthcheck() -> Response[str]:
    return Response(content="OK", status_code=status_codes.HTTP_200_OK, media_type=MediaType.TEXT)
