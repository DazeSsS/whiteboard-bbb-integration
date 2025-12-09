from pydantic import BaseModel

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    AlreadyExistsException,
    CodeFailed,
    NotFoundException
)


class ErrorResponse(BaseModel):
    detail: str


def set_exceptions(app: FastAPI):
    @app.exception_handler(CodeFailed)
    async def code_failed_exception_handler(request: Request, exc: CodeFailed):
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(detail=exc.detail).model_dump()
        )
    
    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(request: Request, exc: NotFoundException):
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(detail=exc.detail).model_dump()
        )

    @app.exception_handler(AlreadyExistsException)
    async def already_exists_exception_handler(request: Request, exc: AlreadyExistsException):
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(detail=exc.detail).model_dump()
        )
