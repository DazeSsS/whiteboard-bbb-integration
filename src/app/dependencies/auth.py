from fastapi import HTTPException, Request

from app.domain.entities import UserData
from app.domain.services.user import UserService


def get_current_user_data(request: Request) -> int:
    token = request.state.token
    if not token:
        raise HTTPException(status_code=401, detail='Authorization token was not provided')
    
    payload = UserService.exctract_jwt_payload(token=token)
    user_id = payload.get('userId')

    return UserData(
        id=user_id,
        token=token
    )
