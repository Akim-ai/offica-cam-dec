from __future__ import annotations

import asyncio

from datetime import datetime as _datetime

from sqlalchemy import Integer, Column, String, ForeignKey, SmallInteger, UniqueConstraint, Boolean, \
    DateTime, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import relationship

from src.Database.Main.DB import DBSession
from src.Database.Main.Mixines.default import CreateTableName
from src.Database.Models.User import Base


class Camera(CreateTableName, Base):
    __table_args__ = {'extend_existing': True}

    id = Column(
        'id', Integer,
        primary_key=True, autoincrement=True,
    )

    frames = relationship('Frame')

    name = Column(
        'name', String(100),
        unique=True, nullable=False
    )
    ip_endpoint = Column(
        'ip_endpoint', String(100),
        nullable=False, unique=True
    )
    is_active = Column(
        'is_active', Boolean,
        nullable=False, default=True
    )

    def __repr__(self):
        return f'{self.id}-{self.name}-{self.ip_endpoint}'


class CameraNeighbours(CreateTableName, Base):

    id = Column(
        'id', Integer, autoincrement=True,
        primary_key=True, unique=True
    )
    left = Column('left', Integer, ForeignKey('camera.id'))
    right = Column('right', Integer, ForeignKey('camera.id'))

    __table_args__ = (
        UniqueConstraint('left', 'right', name='left_right'),
        {'extend_existing': True},

    )

    def __repr__(self):
        return f'{self.left}<->{self.right}'


class DetectedBox(CreateTableName, Base):
    __table_args__ = {'extend_existing': True}

    id = Column(
        'id', Integer,
        autoincrement=True, primary_key=True,
        unique=True
    )
    frame = Column('frame', Integer, ForeignKey('frame.id'))
    top_x = Column('top_x', SmallInteger)
    top_y = Column('top_y', SmallInteger)
    bot_x = Column('bot_x', SmallInteger)
    bot_y = Column('bot_y', SmallInteger)
    detected_user = Column(
        'user', Integer,
        ForeignKey('user.id'), nullable=True
    )

    def __repr__(self):
        return f'{self.id}-user={self.detected_user}-{self.frame}'


class Frame(CreateTableName, Base):
    __table_args__ = {'extend_existing': True}

    id = Column(
        'id', Integer,
        autoincrement=True, primary_key=True,
        unique=True
    )
    frame = Column('frame', String(400), nullable=False)
    # next_frame = Column('next_frame', ForeignKey('frame.id'), nullable=True)
    camera = Column('camera', Integer, ForeignKey('camera.id'))
    boxes = relationship(DetectedBox)
    created_at = Column('created_at', DateTime(timezone=True),)

    def __repr__(self):
        return f'{self.id}-{self.created_at}-{self.camera}'


if __name__ == '__main__':
    
    async def make_migrations():
        session: async_sessionmaker[AsyncSession] = await DBSession().get_session
        with create_engine(
            url='postgresql+psycopg2://your_username:your_password@localhost:5432/your_database', echo=True
        ).begin() as conn:
            print(Base.metadata.tables)
            Base.metadata.create_all(conn)
        async with session() as conn:
            conn: AsyncSession
            # camera = Camera(ip_endpoint='192.168.43.155:81/capture', name='1')
            # conn.add(camera)
            # await conn.commit()
            # result = await conn.execute(select(Camera))
            # await conn.commit()
            # [print(i) for i in result.fetchall()]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(make_migrations())
