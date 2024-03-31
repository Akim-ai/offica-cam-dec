import asyncio

from dotenv import load_dotenv
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from src.image_processing.data_process.src.FrameProcessorController import FrameProcessorController
from src.shared.RabbitMQQueues.image_processing.data_process_queues import (
    queue_run_image_processing, queue_create_image_processor
)
from src.shared.RabbitMQExchange import exch as exchange
from src.shared.datatypes.data_process.interface import IDataProcessFrameProcessFactory

broker = RabbitBroker()
FPC = FrameProcessorController(broker=broker)
app = FastStream(broker)


# def run_process():
#     image_processing_app_runner()
#     # process = Process(target=image_processing_app_runner)
#     # process.start()
#     # return process
#
#
# def image_processing_app_runner():
#     asyncio.run(run_image_process())

@app.on_startup
async def run_image_process():

    async def create_annotation(_broker):
        async def run():
            await FPC.run()

        async def frame_processor_factory(msg: str | dict):
            data: IDataProcessFrameProcessFactory = IDataProcessFrameProcessFactory.model_validate_json(msg)
            if data:
                data = IDataProcessFrameProcessFactory.model_validate_json(msg)
                print(data, type(data))
                await FPC.frame_processor_factory(data=data)
            return

        _broker.subscriber(queue=queue_create_image_processor, exchange=exchange)(frame_processor_factory)
        _broker.subscriber(queue=queue_run_image_processing, exchange=exchange)(run)


    await create_annotation(_broker=broker)


@app.after_startup
async def a():
    print('image_processing_started')
    # data: IDataProcessFrameProcessFactory = IDataProcessFrameProcessFactory(id_=1)
    await FPC.async_init()
    # data1: IDataProcessFrameProcessFactory = IDataProcessFrameProcessFactory(id_=2)
    # await broker.publish(data.model_dump_json(), queue=queue_create_image_processor, exchange=exchange)
    # await broker.publish(data1.model_dump_json(), queue=queue_create_image_processor, exchange=exchange)
    # await broker.publish()


async def runner():
    await run_image_process()
    print('Image processing is started')
    load_dotenv('process.env')
    await app.run()


if __name__ == '__main__':

    asyncio.run(runner())
