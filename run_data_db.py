import asyncio

from faststream import FastStream
from src.Database.src.Views.CameraView import create_camera_annotations
from src.Database.src.Views.FrameView import create_frame_annotations
from src.Database.src.Views.UserView import create_user_annotations
from src.shared.RabbitMQBroker import broker

app = FastStream(broker)


async def runner():
    await create_camera_annotations(_broker=broker)
    await create_frame_annotations(_broker=broker)
    await create_user_annotations(_broker=broker)
    await app.run()


if __name__ == '__main__':
    asyncio.run(runner())
