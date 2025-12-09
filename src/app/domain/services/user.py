from faker import Faker

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings

from app.data.models import User
from app.data.repositories import UserRepository
from app.domain.entities import UserCreate, UserResponse
from app.domain.exceptions import AlreadyExistsException, NotFoundException


class UserService:
    def __init__(
        self,
        session: AsyncSession,
        user_repo: UserRepository,
    ):
        self.session = session
        self.user_repo = user_repo
        self.faker = Faker()

    async def get_user(self, internal_ID: int) -> UserResponse:
        user = self.user_repo.get_by_internal_ID(internal_ID=internal_ID)

        if user is None:
            raise NotFoundException(entity_name='User')

        return UserResponse.model_validate(user)

    async def create_user(self, user: UserCreate) -> UserResponse:
        user_dict = user.model_dump()
        user_obj = User(**user_dict)
        user_obj.name = self.faker.name()

        try:
            async with self.session.begin():
                await self.user_repo.add(user_obj)
                new_user = UserResponse.model_validate(user_obj)
            return new_user
        except IntegrityError:
            raise AlreadyExistsException(entity_name='User')
