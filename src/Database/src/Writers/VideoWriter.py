import datetime
import os

from numpy import ndarray
from vidgear.gears import WriteGear

from src.Database.src.Writers.utils.recursive_path_creator import recursive_folder_creator


class VideoWriter:

    __cam_id: int
    __path: str

    __video_duration: int = 5
    __last_processed: datetime.datetime = datetime.datetime.now() - datetime.timedelta(seconds=__video_duration)

    __video_cnt: int = 0
    __writer: WriteGear = WriteGear

    def __init__(self, cam_id):
        self.__cam_id = cam_id
        self.__relative_path = f'/{self.__cam_id}/'
        self.__path: str = f'{os.getcwd()}+{self.__relative_path}'

    @staticmethod
    def __reformat_datetime_to_folders_path(_datetime: datetime.datetime):
        return _datetime.strftime('%Y/%m/%d/')

    def __check_create_path(self) -> str:
        path: str = os.path.join(self.__path, self.__reformat_datetime_to_folders_path(self.__last_processed))
        recursive_folder_creator(path=path)
        return path

    def __check_recreate_writer(self):
        current_video_end = self.__last_processed + datetime.timedelta(seconds=self.__video_duration)
        if current_video_end > datetime.datetime.now() + datetime.timedelta(seconds=1):
            return
        self.__video_cnt += 1
        if self.__video_cnt != 1:
            self.__writer.close()
        path = self.__check_create_path()
        self.__last_processed = datetime.datetime.now() + datetime.timedelta(
            seconds=self.__video_duration+self.__video_duration / 2
        )
        seconds = self.__last_processed.second // self.__video_duration
        output_params = {
            "-input_framerate": 3.5,
            "-output_dimensions": (640, 480),
         }
        self.__writer = WriteGear(
            output=os.path.join(
                path,
                f'{self.__last_processed.strftime("%H_%M")}_{seconds}.mp4'
            ),
            **output_params,
        )

    def write(self, frame: ndarray):
        self.__check_recreate_writer()
        self.__writer.write(frame=frame)








