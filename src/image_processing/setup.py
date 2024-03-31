from src.image_processing.Camera.camera_controller.CameraController import CameraController


class ImageProcessingAppConfig:

    camera_controller: CameraController

    def __new__(cls, *args, **kwargs):
        it = cls.__dict__.get('__it__')
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.__init()
        return it

    def __init(self):
        self.camera_controller = CameraController()
