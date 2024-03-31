class DBConfig:
    MAIN_DB_CONNECTION_STRING: str

    def __new__(cls, *args, **kwargs):
        it = cls.__dict__.get('__it__')
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.__init(connection_string=kwargs.get('connection_string'))
        return it

    def __init(self, connection_string: str):
        self.MAIN_DB_CONNECTION_STRING = connection_string
