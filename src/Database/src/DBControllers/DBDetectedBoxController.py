from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.Database.Loggers import DetectedBoxLogger
from src.Database.src.DBControllers.Abstract.SessionManager import SessionManager
from src.image_processing.shared.datatypes.db.IDetectedBox import IDetectedBoxList


class DBDetectedBoxController(SessionManager):
    session: async_sessionmaker[AsyncSession]
    __logger = DetectedBoxLogger

    async def create_boxes(self, data: IDetectedBoxList):
        async with self.session.begin() as conn:
            conn: AsyncSession
            for box in data.boxes:
                conn.add(box.to_db_detected_box())
            await conn.commit()
        self.__logger.log('debug', message='detected box -> created')
