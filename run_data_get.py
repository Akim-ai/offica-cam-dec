import asyncio

from faststream import FastStream
from faststream.rabbit import RabbitBroker
from src.shared.RabbitMQExchange import exch as exchange
from src.image_processing.data_get.src.DataGetController import DataGetController
from src.shared.RabbitMQQueues.image_processing.data_get_queues import queue_create_data_get
from src.shared.RabbitMQQueues.image_processing.data_process_queues import queue_image_process_result

broker = RabbitBroker()
app = FastStream(broker)
DGC = DataGetController(broker=broker)


async def result(res):
    print(res)
    return


@app.on_startup
async def _test():
    broker.subscriber(queue=queue_create_data_get, exchange=exchange)(DGC.data_get_factory)
    broker.subscriber(queue=queue_image_process_result, exchange=exchange)(result)
    # await broker.start()
    # data: IDataProcessFrameProcessFactory = IDataProcessFrameProcessFactory(id_=1)
    # data1: IDataProcessFrameProcessFactory = IDataProcessFrameProcessFactory(id_=2)
    # await broker.publish(data.model_dump_json(), queue=queue_create_image_processor, exchange=exchange, reply_to=queue_image_process_result)
    # await broker.publish(data1.model_dump_json(), queue=queue_create_image_processor, exchange=exchange, reply_to=queue_image_process_result)
    # await broker.publish(IDataGetFactory.model_validate_json(json.dumps(
    #     {'id_': 1, 'local_address': '192.168.43.155:81/capture'})), queue=queue_create_data_get, exchange=exchange)
    # await asyncio.sleep(
    #     10, result=
    #     await broker.publish({'id_': 2, 'local_address': '192.168.43.155:81/capture'}, queue=queue_create_data_get, exchange=exchange)
    # )

    # await broker.publish()


@app.after_startup
async def after_start():
    await DGC.async_init()


async def runner():
    await app.run()


if __name__ == '__main__':
    asyncio.run(runner())
