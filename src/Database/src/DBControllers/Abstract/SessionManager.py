from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.Database.Main.DB import DBSession


class SessionManager:

    session: async_sessionmaker[AsyncSession]

    async def async_init(self):
        self.session = await DBSession().get_session

