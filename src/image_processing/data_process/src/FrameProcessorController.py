import asyncio

import aioredis
from faststream.rabbit import RabbitBroker

from src.image_processing.data_process.src.FaceIdentification import FaceIdentification
from src.image_processing.data_process.src.FrameProcessor import FrameProcessor
import logging

from src.shared.RabbitMQBroker import broker
from src.shared.RabbitMQExchange import exch
from src.shared.RabbitMQQueues.db_data_queues import queue_get_frame_processors
from src.shared.datatypes.data_process.interface import IDataProcessFrameProcessFactory, \
    IDataProcessFrameProcessFactoryList


class FrameProcessorController:

    __frame_processors: dict[int: FrameProcessor] = {}
    __run: bool = False
    __logger: logging.Logger
    __broker: RabbitBroker
    __face_identification: FaceIdentification

    def __new__(cls, *args, **kwargs):
        it = cls.__dict__.get('__it__')
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.__init(*args, **kwargs)
        return it

    def __init(self, *args, **kwargs):
        self.__redis = aioredis.from_url("redis://localhost")
        self.__init_logger()
        self.__broker = broker
        self.__frame_processors = {}
        self.__face_identification = FaceIdentification(broker=self.__broker)

    def __del__(self):
        self.__redis.close()

    async def async_init(self):
        await self.__broker.start()
        await self.__face_identification.async_init()

        frame_processors = await self.__broker.publish('', queue=queue_get_frame_processors, exchange=exch, rpc=True)
        if not frame_processors:
            return
        await self.__create_frame_processors(frame_processors)

    async def __create_frame_processors(self, frame_processors: str):
        print(frame_processors)
        frame_processors = IDataProcessFrameProcessFactoryList.model_validate_json(json_data=frame_processors)
        if not frame_processors:
            return
        print(frame_processors)
        for i in frame_processors.frame_processors:
            i: IDataProcessFrameProcessFactory
            print(i)
            await self.frame_processor_factory(data=i)

        await self.run()

    async def close(self):
        await self.__redis.close()

    def __init_logger(self):
        self.__logger = logging.getLogger('Frame_Processor')
        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler('logs.txt')

        stream_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        stream_handler.setFormatter(stream_format)
        file_handler.setFormatter(file_format)

        self.__logger.addHandler(stream_handler)
        self.__logger.addHandler(file_handler)

    async def __add_frame_processor(self, frame_processor: FrameProcessor):
        self.__frame_processors.update({frame_processor.id_: frame_processor})
        if not self.__run:
            self.__run = True
        self.__logger.info('Created new image processor')

    def remove_frame_processor(self, data: IDataProcessFrameProcessFactory):
        self.__frame_processors.pop(data.id_)
        if not self.__frame_processors:
            self.__run = False
        self.__logger.info(f'Removed image processor {data.id_}')

    async def frame_processor_factory(self, data: IDataProcessFrameProcessFactory):
        frame_processor = FrameProcessor(
            redis=self.__redis, id_=data.id_,
            logger=self.__logger, broker=self.__broker,
            face_identification=self.__face_identification,
        )
        await self.__add_frame_processor(frame_processor=frame_processor)

    async def run(self, *args, **kwargs):
        # print('runs')
        while self.__run:
            for processor in tuple(self.__frame_processors.values()):
                processor: FrameProcessor
                await processor.process_data()
                # await asyncio.sleep(2)
            # print('1')
            # await asyncio.sleep(0.1)

