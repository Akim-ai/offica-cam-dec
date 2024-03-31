import asyncio
from datetime import datetime, time, timedelta, timezone, tzinfo
import json
from pprint import pprint

from sqlalchemy import select, text
from sqlalchemy.event import contains
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.baked import Result

from src.Database.Loggers import FrameLogger
from src.Database.Models.Camera import Frame, DetectedBox
from src.Database.src.DBControllers.Abstract.SessionManager import SessionManager
from src.Database.src.Views.UserView import create_detected_user
from src.Database.src.Writers.FrameWriter.FrameWriterController import FrameWriterController
from src.Database.src.Writers.Reader import read_to_hex
from src.shared.datatypes.api.FrameViewTypes import StartTimeIn, StartTimeByUser
from src.shared.datatypes.db import IFrameWithBoxes
from src.shared.datatypes.db.IFrame import IFrame
from src.shared.datatypes.json_encoders_decoders.datetime import convert_datetime_to_iso_8601_with_z_suffix
from zoneinfo import ZoneInfo


class DBFrameController(SessionManager):

    session: async_sessionmaker[AsyncSession]

    __writers_controller: FrameWriterController = FrameWriterController()
    __logger = FrameLogger

    async def create_frame(self, data: IFrame):
        path = await self.__writers_controller.write(frame=data.frame, prefix=data.camera, processed_time=data.created_at)
        self.__logger.log('debug', message='frame -> written')
        
        raw_frame_insert = """
            INSERT INTO frame (frame, camera, created_at)
            VALUES (:frame, :camera, :created_at)
        """
        async with self.session() as conn:
            conn: AsyncSession
            print(str(data.created_at))
            await conn.execute(text(raw_frame_insert), {
                "camera": data.camera,
                "created_at": data.created_at,
                "frame": path
            })
            await conn.commit()
        self.__logger.log('debug', message='frame -> created')

    async def create_frame_with_boxes(self, data: IFrameWithBoxes):

        await self.create_frame(data=data.frame)

        async with self.session() as conn:
            frame: IFrame = data.frame
            self.__logger.log('debug', message='frame -> created')
            frame: Result = await conn.execute(select(Frame).where(
                Frame.camera == frame.camera,
                Frame.created_at == frame.created_at
            ).limit(1))
            frame: IFrame = frame.first()[0]
            for box in data.boxes:
                db_box: DetectedBox = box.to_db_box()
                db_box.frame = frame.id
                print(box.detected_user)
                conn.add(db_box)
            await conn.commit()
            self.__logger.log('debug', message='detected boxes -> created')

    async def get_frames(self, data: StartTimeIn):
        raw_frames = """
        SELECT
            frame.frame,
            frame.created_at,
            json_agg(
                json_build_object(
                    'top_x', detected__box.top_x,
                    'top_y', detected__box.top_y,
                    'bot_x', detected__box.bot_x,
                    'bot_y', detected__box.bot_y,
                    'user_id', detected__box."user"
                )
            ) AS boxes
        FROM
            frame
        LEFT JOIN 
            detected__box ON detected__box.frame = frame.id 
        WHERE 
            frame.camera = :camera_id AND
            frame.created_at > TO_TIMESTAMP('{0}', 'YYYY-MM-DD HH24:MI:SS.US') AT TIME ZONE 'UTC' AND
            frame.created_at <= TO_TIMESTAMP('{1}', 'YYYY-MM-DD HH24:MI:SS.US') AT TIME ZONE 'UTC'
        GROUP BY
            frame.frame, frame.created_at
        """
        time_offset: int = 10
        data.start = data.start.replace(tzinfo=timezone.utc)
        start_time = data.start - timedelta(seconds=time_offset*2-5)
        end_time = data.start - timedelta(seconds=time_offset*1-5)
        raw_frames = raw_frames.format(str(start_time), (end_time))
        async with self.session() as conn:
            print(data.camera_id)
            joined_result = await conn.execute(
                text(raw_frames),
                {
                    'camera_id': data.camera_id,
                }
            )
            result = joined_result.fetchall()
            frames = [
                {
                    'frame': row[0],
                    'created_at': row[1],
                    'boxes': row[2]
                } for row in result
            ]
            _result = {
                    "next": (end_time + timedelta(seconds=time_offset*2)).isoformat(),
                    "data": frames,
                }
            return _result 
    
    async def get_frames_by_user(self, data: StartTimeByUser):
        raw_get_frames_by_user = """
        SELECT
            frame.frame,
            frame.created_at,
            json_agg(
                json_build_object(
                    'top_x', detected__box.top_x,
                    'top_y', detected__box.top_y,
                    'bot_x', detected__box.bot_x,
                    'bot_y', detected__box.bot_y,
                    'user_id', detected__box."user"
                )
            ) AS boxes
        FROM
            frame
        JOIN detected__box ON detected__box.frame = frame.id
        WHERE frame.id IN (
            SELECT DISTINCT frame
            FROM detected__box
            WHERE "user" = :user_id
        )   AND
            frame.created_at > TO_TIMESTAMP('{0}', 'YYYY-MM-DD HH24:MI:SS.US') AT TIME ZONE 'UTC' AND
            frame.created_at <= TO_TIMESTAMP('{1}', 'YYYY-MM-DD HH24:MI:SS.US') AT TIME ZONE 'UTC'
        GROUP BY
            frame.frame, frame.created_at
        """
        time_offset: int = 10
        data.start = data.start.replace(tzinfo=timezone.utc)
        start_time = data.start - timedelta(seconds=time_offset*2-5)
        end_time = data.start - timedelta(seconds=time_offset*1-5)
        raw_get_frames_by_user = raw_get_frames_by_user.format(str(start_time), (end_time))
        async with self.session() as conn:
            result = await conn.execute(
                text(raw_get_frames_by_user),
                {
                    "user_id": data.user_id
                },
            )
            result = result.all()
            frames = [
                {
                    'frame': row[0],
                    'created_at': row[1],
                    'boxes': row[2]
                } for row in result ]
            _result = {
                    "next": (end_time + timedelta(seconds=time_offset*2)).isoformat(),
                    "data": frames,
                }
            print(f'{_result=}')
            return _result
