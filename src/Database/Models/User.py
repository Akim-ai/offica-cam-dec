import asyncio
import hashlib

from sqlalchemy import Column, Integer, String, create_engine, Boolean
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.Database.Main.DB import DBSession
from src.Database.Main.Mixines.default import CreateTableName
from src.Database.Main.base import Base


class User(CreateTableName, Base):
    id = Column(
        'id', Integer,
        primary_key=True, autoincrement=True,
    )

    password = Column(
        'password', String(255),
        nullable=True
    )

    first_name = Column(
        'first_name', String(50),
        nullable=True
    )

    last_name = Column(
        'last_name', String(50),
        nullable=True
    )
    detected_path_image = Column(
        'detected_path_image', String(200),
        nullable=False
    )
    is_disabled = Column(
        'is_disabled', Boolean,
        default=False
    )
    username = Column(
        'username', String(50),
        nullable=True
    )

    @staticmethod
    def __hash_password(password: str) -> str:
        hash_object = hashlib.sha512()

        # Encode the password to bytes and hash it
        hash_object.update(password.encode('utf-8'))

        # Return the hexadecimal representation of the hash
        return hash_object.hexdigest()

    def set_password(self, password: str) -> None:
        hashed_password = self.__hash_password(password=password)
        self.password = hashed_password

    def check_password(self, password: str) -> bool:
        return self.__hash_password(password=password) == self.password


if __name__ == '__main__':
    async def make_migrations():
        session: async_sessionmaker[AsyncSession] = await DBSession().get_session
        with create_engine(
            url='postgresql+psycopg2://your_username:your_password@localhost:5432/your_database', echo=True
        ).begin() as conn:
            Base.metadata.drop_all(conn)
            print(Base.metadata.tables)
        async with session() as conn:
            test_user = User()
            # test_user.first_name = 'name'
            # test_user.last_name = 'l_name'
            # test_user.set_password('123')
            # conn.add(test_user)
            # await conn.commit()


    asyncio.run(make_migrations())
