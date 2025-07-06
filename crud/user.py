from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute, subqueryload

from api.security.hash import Hash
from models import CreateUser, UpdateUser, User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: CreateUser) -> int:
        user_dict = user.model_dump()
        hashed_password = Hash(user_dict.pop("password"))
        user_dict["hashed_password"] = hashed_password()
        new_user = User(**user_dict)
        self.session.add(new_user)
        await self.session.commit()
        return new_user.id

    async def _get_user(self, value: str | int, field: str) -> Optional[User]:
        allowed_fields = {"email", "id", "username"}
        if field not in allowed_fields:
            raise ValueError("Invalid field")

        column = getattr(User, field, None)
        if not isinstance(column, InstrumentedAttribute):
            raise ValueError(f"{field} is not a valid SQLAlchemy column")

        stmt = (
            select(User).where(column == value).options(subqueryload(User.environments))
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self._get_user(email, "email")

    async def get_by_id(self, user_id: int) -> Optional[User]:
        return await self._get_user(user_id, "id")

    async def get_by_username(self, username: str) -> Optional[User]:
        return await self._get_user(username, "username")

    async def update(self, user: UpdateUser) -> Optional[User]:
        user_dict = user.model_dump()
        old_user = await self.get_by_id(user.id)
        if old_user:
            for key, value in user_dict.items():
                if key == "password":
                    hashed_password = Hash(value)
                    setattr(old_user, "hashed_password", hashed_password())
                    continue
                setattr(old_user, key, value)
            await self.session.commit()
        return old_user

    async def delete(self, user_id: int) -> bool:
        del_user = await self.get_by_id(user_id)
        if del_user:
            await self.session.delete(del_user)
            await self.session.commit()
            return True
        return False
