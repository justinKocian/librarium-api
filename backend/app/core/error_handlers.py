from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core import exceptions
import logging

logger = logging.getLogger(__name__)

def register(app: FastAPI):
    @app.exception_handler(exceptions.AlreadyExistsException)
    async def already_exists_handler(request: Request, exc: exceptions.AlreadyExistsException):
        logger.warning(f"AlreadyExistsException: {exc.detail}")
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(exceptions.NotFoundException)
    async def not_found_handler(request: Request, exc: exceptions.NotFoundException):
        logger.info(f"NotFoundException: {exc.detail}")
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(exceptions.UnauthorizedException)
    async def unauthorized_handler(request: Request, exc: exceptions.UnauthorizedException):
        logger.warning(f"UnauthorizedException: {exc.detail}")
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(exceptions.ForbiddenException)
    async def forbidden_handler(request: Request, exc: exceptions.ForbiddenException):
        logger.warning(f"ForbiddenException: {exc.detail}")
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(exceptions.BadRequestException)
    async def bad_request_handler(request: Request, exc: exceptions.BadRequestException):
        logger.info(f"BadRequestException: {exc.detail}")
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(exceptions.UnprocessableEntityException)
    async def unprocessable_handler(request: Request, exc: exceptions.UnprocessableEntityException):
        logger.info(f"UnprocessableEntityException: {exc.detail}")
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
