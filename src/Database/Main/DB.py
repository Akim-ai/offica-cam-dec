import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession


class DBEngine:

    __engine: AsyncEngine

    def __new__(cls, *args, **kwargs):
        it = cls.__dict__.get('__it__')
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.__init()
        return it

    def __init(self):
        # load_dotenv('./././envs/database.env')
        # database_key = os.getenv('MAIN_DB_CONNECTION_STRING')
        self.__engine: AsyncEngine = create_async_engine(
            # database_key,
            'postgresql+asyncpg://your_username:your_password@localhost:5432/your_database',
            #echo=True,
        )

    @property
    def engine(self):
        return self.__engine


class DBSession:

    __DBEngine: AsyncEngine

    def __init__(self):
        self.__DBEngine = DBEngine()

    def __async_session_generator(self) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(self.__DBEngine.engine, expire_on_commit=False)

    @property
    async def get_session(self) -> async_sessionmaker[AsyncSession]:
        return self.__async_session_generator()
