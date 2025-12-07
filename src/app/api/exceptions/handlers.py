from pydantic import BaseModel

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.exceptions.bbb import CodeFailed


class ErrorResponse(BaseModel):
    detail: str


def set_exceptions(app: FastAPI):
    @app.exception_handler(CodeFailed)
    async def code_failed_exception_handler(request: Request, exc: CodeFailed):
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(detail=exc.detail).model_dump()
        )
