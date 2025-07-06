from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from crud.user import UserRepository
from models import CreateEnvironment, TradingEnvironment, UpdateEnvironment


class EnvironmentService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)

    async def create_environment(
        self, env: CreateEnvironment
    ) -> Optional[TradingEnvironment]:
        user = await self.user_repo.get_by_id(env.user_id)
        if user:
            new_trading_environment = TradingEnvironment(**env.model_dump())
            self.session.add(new_trading_environment)
            await self.session.commit()
            await self.session.refresh(new_trading_environment)
            return new_trading_environment
        return None

    async def get_environment_by_id(self, id_env: int) -> Optional[TradingEnvironment]:
        stmt = (
            select(TradingEnvironment)
            .where(TradingEnvironment.id == id_env)
            .options(joinedload(TradingEnvironment.owner))
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_environment_by_account(
        self, account: str
    ) -> Optional[TradingEnvironment]:
        stmt = (
            select(TradingEnvironment)
            .where(TradingEnvironment.account_api_id == account)
            .options(joinedload(TradingEnvironment.owner))
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_environments_by_user(
        self, user_id: int
    ) -> Sequence[TradingEnvironment]:
        stmt = select(TradingEnvironment).where(TradingEnvironment.user_id == user_id)
        result = await self.session.execute(stmt)
        res = result.scalars().all()
        return res

    async def update_environment(
        self, env: UpdateEnvironment
    ) -> Optional[TradingEnvironment]:
        env_dict = env.model_dump()
        old_env = await self.get_environment_by_id(env.id)
        if old_env:
            for key, value in env_dict.items():
                if key == "user_id":
                    continue
                setattr(old_env, key, value)
            await self.session.commit()
            await self.session.refresh(old_env)
            return old_env
        return None
