from datetime import datetime, timedelta, timezone
from io import BytesIO
from logging import Logger
from typing import Union, Type, Optional

import numpy as np
from PIL import Image
from aioredis import Redis
from faststream.rabbit import RabbitBroker
from numpy._typing import NDArray
from ultralytics.engine.results import Results, Boxes

from src.image_processing.data_process.src.AI.YOLODefaultModel import DefaultDetectionModel
from src.Database.src.Writers.VideoWriter import VideoWriter
from src.image_processing.data_process.src.FaceIdentification import FaceIdentification
from src.image_processing.data_process.src.utils.resize import resize
from src.shared.RabbitMQExchange import exch
from src.shared.RabbitMQQueues.db_data_queues import queue_create_frame, \
    queue_create_frame_with_boxes
from src.shared.datatypes.RawImage import RawImage
from src.shared.datatypes.db import IFrame, IBox, IFrameWithBoxes, IUserWithImage


class FrameProcessor:
    __redis: Redis
    id_: int
    __redis_key: str
    __last_process: datetime
    __logger: Logger

    __save_video: bool = False
    __video_writer: Union[VideoWriter, Type[VideoWriter]] = VideoWriter

    __save_frames: bool = True

    ai_model = DefaultDetectionModel('yolov8n.pt')

    def __init__(
            self, redis: Redis, id_: int,
            logger: Logger, broker: RabbitBroker,
            face_identification: FaceIdentification,
    ):
        self.__redis = redis
        self.id_ = id_
        self.__redis_key = f'{self.id_}_image'
        self.__last_process = datetime.now(timezone.utc)-timedelta(seconds=15)
        self.__logger = logger
        self.__broker = broker
        self.__face_identification = face_identification


    async def __get_frame(self) -> Optional[RawImage]:
        data: str = await self.__redis.get(self.__redis_key)
        if not data:
            return None
        data: RawImage = RawImage.model_validate_json(data)
        data.time = datetime.fromisoformat(data.time)
        await self.__redis.set(self.__redis_key, '')
        if data and data.time < self.__last_process:
            print(f'expired {self.__last_process} {not not data} {data.time}')
            return None
        return data

    @staticmethod
    def __prepare_frame(data: RawImage) -> NDArray:
        bytes_image = bytes.fromhex(data.image)
        image = Image.open(BytesIO(bytes_image))
        image = image.resize((640, 480))
        frame = np.asarray(image, dtype=np.uint8)
        return frame

    async def process_data(self):
        self.__logger.debug(f'{self.id_} processed image')
        data = await self.__get_frame()
        if not data:
            return
        frame = self.__prepare_frame(data=data)

        detected: list[Results] = self.ai_model.track(
            source=frame, classes=[0, ], task='detect', show_labels=False, show_boxes=True,
            show_conf=False, persist=True,
            )
        print('saving')
        # result_frame = frame
        saving_frame = IFrame(camera=self.id_, frame=data.image, created_at=data.time)
        boxes: list[IBox] = []

        for r in detected:
            if not r.boxes:
                continue
            for box in r.boxes:
                box: Boxes
                xyxy = [int(i) for i in box.xyxy[0]]

                saving_box: IBox = IBox(
                        top_x=xyxy[0],
                        top_y=xyxy[1],
                        bot_x=xyxy[2],
                        bot_y=xyxy[3],
                    )

                # Face recognition
                box = resize(frame, xyxy[0], xyxy[2], xyxy[1], xyxy[3])
                user_id = await self.__face_identification.detect_faces(box)
                print(user_id)
                if not user_id:
                    # await self.__broker.publish(
                      #       message=IUserWithImage(
                       #              first_name='Anonymous',
                        #             last_name='',
                         #            detected_image=data.image
                          #       ),
                          #   queue=queue_create_user
                        # )
                    pass
                elif user_id and user_id != -1:
                    saving_box.detected_user = user_id

                boxes.append(saving_box)

        if boxes:
            await self.__broker.publish(
                    message=IFrameWithBoxes(frame=saving_frame, boxes=boxes).model_dump_json(),
                    queue=queue_create_frame_with_boxes, exchange=exch,
                    )
            return

        await self.__broker.publish(message=saving_frame.model_dump_json(), queue=queue_create_frame, exchange=exch)
