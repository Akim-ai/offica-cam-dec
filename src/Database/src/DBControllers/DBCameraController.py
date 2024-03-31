import json

from pydantic import NonNegativeInt
from sqlalchemy import select, desc, Result, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.sql.functions import count

from src.Database.Loggers import CameraLogger
from src.Database.Models.Camera import Camera
from src.Database.src.DBControllers.Abstract.SessionManager import SessionManager
from src.shared.RabbitMQBroker import broker
from src.shared.RabbitMQExchange import exch
from src.shared.RabbitMQQueues.image_processing.data_get_queues import queue_create_data_get
from src.shared.RabbitMQQueues.image_processing.data_process_queues import queue_create_image_processor
from src.shared.datatypes.api.Pagination import Paginator
from src.shared.datatypes.db.ICamera import ICamera
from src.shared.datatypes.data_get.IDataGetFactory import IDataGetFactoryList, IDataGetFactory
from src.shared.datatypes.data_process.interface import IDataProcessFrameProcessFactory, \
    IDataProcessFrameProcessFactoryList


class DBCameraController(SessionManager):

    session: async_sessionmaker[AsyncSession]
    __broker = broker
    __logger = CameraLogger
    __offset: int = 20
    __limit: int = 20

    async def async_init(self):
        await super().async_init()
        await self.__broker.start()

    async def get_all_frame_processors(self):
        frame_process_container = IDataProcessFrameProcessFactoryList()

        async with self.session() as conn:
            conn: AsyncSession
            cameras = await conn.execute(select(Camera.id).where(Camera.is_active==True))
            for camera in cameras.all():
                frame_process = IDataProcessFrameProcessFactory(id_=camera[0])
                frame_process_container.frame_processors.append(frame_process)

        _json = frame_process_container.model_dump_json()
        self.__logger.log('debug', message='given all frame processors')
        return _json

    async def get_all_data_gets(self):
        data_get_container = IDataGetFactoryList()
        print('all_data_gets')
        async with self.session() as conn:
            conn: AsyncSession
            cameras = await conn.execute(select(Camera.id, Camera.ip_endpoint).where(Camera.is_active==True))
            for camera in cameras.all():
                data_get = IDataGetFactory(id_=camera[0], local_address=camera[1])
                data_get_container.data_get_factory_data.append(data_get)

        _json = data_get_container.model_dump_json()
        self.__logger.log('debug', message='given all data gets')
        return _json

    async def create_camera(self, data: ICamera):
        camera = data.to_db_camera()
        async with self.session() as conn:
            conn: AsyncSession
            conn.add(camera)
            data = await conn.commit()
            self.__logger.log('debug', message='camera created')
            print(data)
            if not camera.is_active:
                return
            created_camera: Result[tuple[Camera]] = await conn.execute(select(Camera).order_by(desc(Camera.id)))
            created_camera: Camera = created_camera.first()[0]
            message = IDataGetFactory(id_=created_camera.id, local_address=created_camera.ip_endpoint)
            await self.__broker.publish(message=message, queue=queue_create_image_processor, exchange=exch)
            self.__logger.log('debug', message='image_processors -> updated')
            message = IDataGetFactory(id_=created_camera.id, local_address=created_camera.ip_endpoint)
            await self.__broker.publish(message=message, queue=queue_create_data_get, exchange=exch)
            self.__logger.log('debug', message='image_getters -> updated')
            return {
                "id": created_camera.id,
                "ip_endpoint": created_camera.ip_endpoint,
                "name": created_camera.name,
            }

    async def get_camera(self, camera_id: int):
        async with self.session() as conn:
            conn: AsyncSession
            camera = await conn.execute(select(Camera).where(Camera.id == camera_id))
            camera: Camera = camera.first()
            if not camera:
                return str({'error': "Doesn't exists"})
            camera = camera[0]
            camera: ICamera = ICamera(id=camera.id, is_active=camera.is_active, ip_endpoint=camera.ip_endpoint, name=camera.name)
            return camera.model_dump()

    async def get_cameras(self, page: NonNegativeInt):
        async with self.session() as conn:
            conn: AsyncSession
            raw_get_all_cams = """
            SELECT id, name, ip_endpoint, is_active
            FROM camera
            WHERE is_active = True
            ORDER BY camera.id DESC
            OFFSET :offset LIMIT :limit;
            
            """

            result_cameras: Result = await conn.execute(text(raw_get_all_cams), {'offset': self.__offset*(page-1), 'limit': self.__limit})
            print(result_cameras)

            if not result_cameras:
                return {'error': "Doesn't exists"}

            raw_get_cams_count = """
            SELECT COUNT(*)
            FROM camera
            """
            result_cnt = await conn.execute(text(raw_get_cams_count))
            cnt = result_cnt.fetchall()
            print(cnt)
            assigner = lambda camera: ICamera(
                    id=camera[0], name=camera[1],
                    ip_endpoint=camera[2], is_active=camera[3]
                )

            result_pagination: dict = Paginator.assign(
                objects=result_cameras,
                assigner=assigner,
                cnt=cnt[0][0],
                offset=self.__offset,
                page=page,
            )
            print(result_pagination)
            return result_pagination

    async def put_camera(self, camera: ICamera):
        raw_update = """
        UPDATE camera
        SET ip_endpoint = :ip_endpoint, is_active = :is_active, name = :name
        WHERE id = :id;
        """
        async with self.session() as conn:
            print(camera)
            await conn.execute(text(raw_update), camera.model_dump())
            await conn.commit()
            return ''
