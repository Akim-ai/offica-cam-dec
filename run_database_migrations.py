import asyncio
import hashlib
from pydantic import main

from sqlalchemy import Column, Integer, String, create_engine, Boolean
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.Database.Main.DB import DBSession
from src.Database.Main.Mixines.default import CreateTableName
from src.Database.Main.base import Base
from src.Database.Models.User import User
from src.Database.Models.Camera import (
        Camera, DetectedBox, Frame,
)


if __name__ == "__main__":
    async def make_migrations():
        session: async_sessionmaker[AsyncSession] = await DBSession().get_session
        with create_engine(
            url='postgresql+psycopg2://your_username:your_password@localhost:5432/your_database', echo=True
        ).begin() as conn:
            Base.metadata.drop_all(conn)
            Base.metadata.create_all(conn)
            print(Base.metadata.tables)
        async with session() as conn:
            # test_user.first_name = 'name'
            # test_user.last_name = 'l_name'
            # test_user.set_password('123')
            # conn.add(test_user)
            # await conn.commit()
            pass

    asyncio.run(make_migrations())
