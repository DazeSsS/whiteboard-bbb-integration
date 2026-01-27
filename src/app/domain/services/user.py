import jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.models import User
from app.data.repositories import UserRepository
from app.domain.entities import UserCreate, UserData, UserResponse
from app.domain.exceptions import AlreadyExistsException, NotFoundException


class UserService:
    def __init__(
        self,
        session: AsyncSession,
        user_repo: UserRepository,
    ):
        self.session = session
        self.user_repo = user_repo

    @staticmethod
    def exctract_jwt_payload(token: str):
        payload = jwt.decode(
            jwt=token,
            options={
                'verify_signature': False
            }
        )
        return payload
    
    async def get_user_token(self, user_id: int) -> str:
        user = await self.user_repo.get_by_id(id=user_id)

        if user is None:
            raise NotFoundException(entity_name='User')

        return user.token

    async def get_user(self, user_id: int) -> UserResponse:
        user = await self.user_repo.get_by_id(id=user_id)

        if user is None:
            raise NotFoundException(entity_name='User')

        return UserResponse.model_validate(user)

    async def create_user(self, user_data: UserData, user: UserCreate) -> UserResponse:
        user_dict = user.model_dump()
        user_obj = User(
            id=user_data.id,
            token=user_data.token,
            **user_dict
        )

        try:
            async with self.session.begin():
                await self.user_repo.add(user_obj)
                new_user = UserResponse.model_validate(user_obj)
            return new_user
        except IntegrityError:
            raise AlreadyExistsException(entity_name='User')
        
    async def update_user_name(self, user_id: int, name: str) -> UserResponse:
        async with self.session.begin():
            updated_user = await self.user_repo.update_name(user_id=user_id, name=name)

            if updated_user is None:
                raise NotFoundException(entity_name='User')
            
            return UserResponse.model_validate(updated_user)
