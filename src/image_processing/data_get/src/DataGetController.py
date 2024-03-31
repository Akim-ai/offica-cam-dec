from asyncio import create_task, gather, sleep

import aioredis
from aiohttp import ClientSession, ClientConnectorError
from faststream.rabbit import RabbitBroker

from src.image_processing.data_get.src.DataGet import DataGet
from src.shared.RabbitMQQueues.db_data_queues import queue_get_all_data_gets
from src.shared.datatypes.data_get.IDataGetFactory import IDataGetFactory, IDataGetFactoryList
from src.shared.RabbitMQExchange import exch as exchange


class DataGetController:
    __data_gets: dict[int: DataGet] = {}
    __data_gets_errors: dict[int: int] = {}
    __session: ClientSession
    __run: bool = False
    __broker: RabbitBroker

    def __new__(cls, *args, **kwargs):
        it = cls.__dict__.get('__it__')
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.__init(*args, **kwargs)
        return it

    def __init(self, **kwargs):
        self.__data_gets = {}
        self.__redis = aioredis.from_url("redis://localhost")
        self.__broker = kwargs.get('broker')

    async def async_init(self):
        self.__session = ClientSession()
        print('async_init')
        await self.__init_data_gets()

    async def __init_data_gets(self):
        data_gets = await self.__broker.publish(
            '', queue=queue_get_all_data_gets,
            exchange=exchange, rpc=True
        )
        print(f'{data_gets=}')
        data_gets = IDataGetFactoryList.model_validate_json(json_data=data_gets)
        if not data_gets:
            return
        print(data_gets)
        for i in data_gets.data_get_factory_data:
            i: IDataGetFactory
            print(i)
            await self.data_get_factory(data=i)

        await self.run()

    async def close(self):
        await self.__session.close()

    async def data_get_factory(self, data: IDataGetFactory):
        data_get: DataGet = DataGet(
            id_=data.id_, local_address=data.local_address,
            session=self.__session, redis=self.__redis,
        )
        await self.__add_data_get(data_get=data_get)

    async def __add_data_get(self, data_get: DataGet):
        self.__data_gets.update({data_get.id_: data_get})
        print(f'updated: {data_get.id_}')
        if not self.__run:
            self.__run = True
            print('runs')

    async def remove_data_get(self, id_: int) -> DataGet:
        data_get = self.__data_gets.pop(id_)
        if not self.__data_gets:
            self.__run = False
        return data_get
    
    async def __prepare_tasks(self):
        data_get: DataGet
        tasks: list = [create_task(data_get.get_data()) for id_, data_get in self.__data_gets.items()]

        return tasks

    async def run(self):
        while self.__run:
            errors = await gather(*await self.__prepare_tasks())
            for e, id_ in errors:
                print(f'{e=}, {id_}')
                if not e:
                    self.__data_gets_errors[id_] = 0

                if e == 111:
                    errors_cnt = self.__data_gets_errors.get(id_, None)
                    if not errors_cnt:
                        self.__data_gets_errors[id_] = 1
                    elif errors_cnt == 2:
                        print(f'poped {id_=}', await self.remove_data_get(id_))
                    else:
                        self.__data_gets_errors[id_] += self.__data_gets_errors[id_]
