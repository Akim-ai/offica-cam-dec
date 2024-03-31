from datetime import datetime

from src.Database.src.Writers.FrameWriter.FrameWriter import FrameWriter


class FrameWriterController:

    __frame_writers = dict[int: FrameWriter]

    def __init__(self):
        self.__frame_writers = {}

    async def write(self, frame: bytes, prefix: str, processed_time: datetime):
        writer = self.__frame_writers.get(prefix)
        if not writer:
            self.__frame_writers.update({prefix: FrameWriter(prefix=prefix)})
            writer: FrameWriter = self.__frame_writers.get(prefix)

        return await writer.write(frame=frame, processed_time=processed_time)
