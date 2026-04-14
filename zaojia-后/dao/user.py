from sqlalchemy import select

from dao.base import BaseDao
from database.db import session
from models.user import UserModel
from schemas.user import DataBaseCreateUser


class UserDao(BaseDao):

    @classmethod
    async def create_user(cls, obj: DataBaseCreateUser):
        new_user = UserModel(**obj.model_dump())
        session.add(new_user)
        await session.commit()

    @classmethod
    async def get_by_id(cls, user_id: str):
        stmt = select(UserModel).filter_by(uid=user_id)
        result = await session.execute(stmt)
        user = result.scalars().first()
        return user

    @classmethod
    async def get_by_username(cls, username: str):
        stmt = select(UserModel).filter_by(username=username)
        result = await session.execute(stmt)
        user = result.scalars().first()
        return user

    @classmethod
    async def update(cls, user):
        session.add(user)
        await session.commit()

    @classmethod
    async def list_user(cls):
        stmt = select(UserModel)
        result = await session.execute(stmt)
        users = result.scalars().all()
        return users


