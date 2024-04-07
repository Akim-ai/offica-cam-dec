import os
import time
from dataclasses import dataclass
from io import BytesIO

from PIL import Image
import numpy as np
from faststream.rabbit import RabbitBroker

import face_recognition
from numpy._typing import NDArray

from src.image_processing.data_process.src.utils.resize import resize
from src.shared.RabbitMQQueues.db_data_queues import queue_get_all_detected_users, queue_create_user
from src.shared.datatypes.db.IUser import IListUserWithImage, IUser, IUserWithImage


@dataclass
class Human:
    detected: str


class FaceIdentification:
    __faces: list
    __ids: list
    __broker: RabbitBroker

    def __new__(cls, *args, **kwargs):
        it = cls.__dict__.get('__it__')
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.__init(*args, **kwargs)
        return it

    def __init(self, broker: RabbitBroker):
        self.__broker = broker
        self.__faces = []
        self.__ids = []

    async def async_init(self):
        detected_faces = await self.__broker.publish('', queue=queue_get_all_detected_users, rpc=True)
        if not detected_faces:
            print('no faces')
            return
        detected_faces = IListUserWithImage.model_validate_json(detected_faces)
        for user in detected_faces.users:
            frame = self.serialize_frame(frame=user.get("detected_image"))
            id_ = user.get("id")
            self.add_new_face(user_id=id_, face=frame)

    @staticmethod
    def serialize_frame(frame) -> NDArray:
        bytes_image = bytes.fromhex(frame)
        image = Image.open(BytesIO(bytes_image))
        frame = np.asarray(image, dtype=np.uint8)
        face_encoding = face_recognition.face_encodings(frame)[0]
        return face_encoding

    def add_new_face(self, user_id, face):
        print(user_id)
        self.__faces.append(face)
        self.__ids.append(user_id)
    
    @staticmethod
    def numpy_array_to_bytes(image_array):
        """Convert a NumPy array to bytes representing a JPEG image."""
        with BytesIO() as buffer:
            img = Image.fromarray(image_array)
            img.save(buffer, format="JPEG")
            return buffer.getvalue()

    async def detect_faces(self, image: np.ndarray):
        compared_image = face_recognition.face_encodings(image)
        if not compared_image:
            """ No Faces """
            return -1
        compared_image = compared_image[0]
        print(type(compared_image))
        matches = face_recognition.compare_faces(self.__faces, compared_image)
        id_ = 0
        if any(matches):
            """ Found face """
            first_match_index = matches.index(True)
            id_ = self.__ids[first_match_index]
            print(f'{id_=} {type(id_)}')
            return id_
        """ Found face but not recognized """
        face_location = face_recognition.face_locations(image)
        print(face_location)
        # TODO loop with anonymous users creation
        # face_location -> list with tuples of (top, right, bottom, left)
        for top, right, bottom, left in face_location:
            print(top, right, bottom, left)
            resized = resize(image=image, x1=left, x2=right, y1=top, y2=bottom)
            bytes_image: bytes = self.numpy_array_to_bytes(resized)
            face_encoding = face_recognition.face_encodings(resized)
            if not face_encoding:
                continue
            face_encoding = face_encoding[0]
            id_ = await self.__broker.publish(
                    message=IUserWithImage(
                        first_name="anonymous",
                        last_name="",
                        detected_image=bytes_image,
                        password=''
                        ).model_dump(),
                    queue=queue_create_user,
                    rpc=True
                    )
            print(type(id_), f"{id_=}")
            id_ = id_.get("id")

            self.add_new_face(user_id=id_, face=face_encoding)

        return id_

    def delete_face(self, id_: int):
        index = self.__ids.index(id_)
        self.__ids.remove(id_)
        self.__faces.pop(index)
