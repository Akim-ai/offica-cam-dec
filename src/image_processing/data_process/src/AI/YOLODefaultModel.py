from ultralytics import YOLO


class DefaultDetectionModel(YOLO):
    def __new__(cls, *args, **kwargs):
        it = cls.__dict__.get('__it__')
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.__init(*args, **kwargs)
        return it

    def __init(self, *args, **kwargs):
        self.model = super().__init__(*args, **kwargs)
