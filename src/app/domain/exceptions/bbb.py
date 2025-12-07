from fastapi import status

from app.shared.exceptions import AppException


class CodeFailed(AppException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )
