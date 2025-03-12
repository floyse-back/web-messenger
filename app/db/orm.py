from sqlalchemy.ext.asyncio import async_sessionmaker,AsyncSession
from ..schemas import UserModel
from sqlalchemy import select
from .models import Users

class UsersCRUD:
    async def insert_user(self,async_session:async_sessionmaker[AsyncSession],user:UserModel):
        async with async_session() as session:
            user_model = Users(
                **user.model_dump()
            )

            session.add(user_model)
            await session.commit()

    async def find_user(self,async_session:async_sessionmaker[AsyncSession],username):
        async with async_session() as session:
            result = await session.execute(select(Users).filter(Users.username == f"{username}"))
            return result.scalars().first()