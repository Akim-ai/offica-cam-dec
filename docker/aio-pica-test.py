import asyncio
import logging
import time

from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitExchange, RabbitQueue

broker = RabbitBroker()
app = FastStream(broker)

exch = RabbitExchange("exchange", auto_delete=True)

queue_1 = RabbitQueue("test-q-1", auto_delete=True)
queue_2 = RabbitQueue("test-q-2", auto_delete=True)


@broker.subscriber(queue_1, exch)
async def base_handler1(msg):
    await asyncio.sleep(10)
    print(msg, 1)


@broker.subscriber(queue_1, exch)  # another service
async def base_handler2(msg):
    print(msg, 2)


@broker.subscriber(queue_2, exch)
async def base_handler3(msg):
    print(msg, 3)


@app.after_startup
async def send_messages():
    await broker.publish(message='1', queue="test-q-1", exchange=exch)  # handlers: 1
    await broker.publish(message='2', queue="test-q-1", exchange=exch)  # handlers: 2
    await broker.publish(message='3', queue="test-q-1", exchange=exch)  # handlers: 1
    await broker.publish(message='4', queue="test-q-2", exchange=exch)  # handlers: 3
    tasks = []
    for i in range(100):
        task = broker.publish(message=f'{i}', queue="test-q-1", exchange=exch)  # handlers: 1
        tasks.append(task)
    await asyncio.gather(*tasks)
    await broker.publish(message='4', queue="test-q-2", exchange=exch)  # handlers: 3

asyncio.run(app.run(log_level=1000))

