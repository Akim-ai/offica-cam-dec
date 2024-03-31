import aiofiles


async def read_to_hex(path: str):
    async with aiofiles.open(path, "rb") as f:
        data = await f.read()
        return data.hex()
