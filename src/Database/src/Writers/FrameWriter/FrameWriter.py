import os
from datetime import datetime, timedelta, timezone

import aiofiles

from src.Database.src.Writers.utils.recursive_path_creator import recursive_folder_creator


class FrameWriter:

    __date = datetime.now(tz=timezone.utc) - timedelta(hours=1)
    __path = __date.strftime('%Y/%m/%d/')

    def __init__(self, prefix: str):
        self.__prefix = prefix
        self.__path = self.__update_path()
        self.cnt = 0

    @property
    def path(self) -> str:
        return self.__path

    @property
    def prefix(self) -> str:
        return self.__prefix

    def set_prefix(self, prefix: str) -> str:
        self.__prefix = prefix
        return self.__prefix

    def __update_path(self, prefix: str = '') -> str:
        self.__path = f'static/{self.__date.strftime("%Y/%m/%d/%H/%M")}/{self.__prefix}/'
        return self.__path

    def __get_check_path(self, processed_time: datetime) -> str:
        if self.__date < processed_time:
            self.__date = processed_time
            self.__update_path()
        recursive_folder_creator(path=self.__path)
        return self.__path

    @staticmethod
    def __get_file_name(processed_time: datetime):
        return f'{processed_time.strftime("%S__%f")}.jpeg'

    async def write(self, frame: bytes, processed_time: datetime) -> str:
        path = f'{self.__get_check_path(processed_time=processed_time)}{self.__get_file_name(processed_time)}'
        async with aiofiles.open(path, 'wb') as out_file:
            await out_file.write(frame)
        return path
