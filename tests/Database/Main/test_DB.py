
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncConnection, AsyncSession

from src.Database.Main.DB import DBEngine, DBSession


class TestDBEngine:

    def test_DBEngine_connection(self):
        engine: AsyncEngine = DBEngine()
        assert isinstance(engine.connect(), AsyncConnection)


class TestDBSession:

    def test_DBSession_connection(self):
        session: AsyncSession = DBSession().get_session()
        print(session.__dict__)

    def test_DBSession_error_handling(self):
        """Tests if the session is closed after error"""
        session: AsyncSession = DBSession().get_session()
        session._is
        try:
            raise Exception('test_exception')
        except Exception as e:
            pass


if __name__ == '__main__':
    TestDBSession().test_DBSession_connection()