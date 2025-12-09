from fastapi import status

from app.shared.exceptions import AppException


class NotFoundException(AppException):
    def __init__(self, entity_name: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity_name} does not exist"
        )

class AlreadyExistsException(AppException):
    def __init__(self, entity_name: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{entity_name} already exists"
        )
