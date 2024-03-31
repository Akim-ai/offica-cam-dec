import asyncio
import ipaddress
import re
import time

from aiohttp import ClientSession, ClientConnectorError, ClientTimeout
from aioredis import Redis

from src.shared.datatypes.RawImage import RawImage


class DataGet:

    __data_source: str
    __session: ClientSession
    __working_protocols: tuple = ('http', 'https')
    __save_video: bool = True

    def __init__(self, id_: int, local_address: str, session: ClientSession, redis: Redis):
        self.id_ = id_
        self.__set_ip_data_source(local_address=local_address)
        self.__session = session
        self.__redis = redis

    async def get_data(self):
        if not self.__data_source:
            raise Exception('No data_source and ip provided')
        try:
            print(f'{self.__data_source=}')
            image_bytes: bytes
            async with self.__session.get(url=self.__data_source, timeout=ClientTimeout(total=2)) as resp:
                # print(f'{self.id_}')
                image_bytes: bytes = await resp.content.read()
            image: RawImage = RawImage(image=image_bytes)
            await self.__redis.set(f'{self.id_}_image', image.model_dump_json())
            print(f'{self.id_}_image')
            return 0, self.id_
        except asyncio.TimeoutError as e:
            return 111, self.id_


    @staticmethod
    def __verify_ip(ip: str) -> bool:
        """ Verifies IPv4 """
        ip_split = re.split(r':|/', ip)
        ip_split_l = len(ip_split)
        match ip_split_l:
            case 0:
                raise Exception('Not valid IP')
            case 1:
                _ip = ip_split[0]
                ipv4 = ipaddress.IPv4Address(_ip)
                if not ipv4.is_private:
                    raise Exception('Not private IP provided')
            case 2:
                """Port or endpoint"""
                port: re.Match = re.fullmatch(r'\d+', ip_split[1])
                if port:
                    port: int = int(port.group())
                    if port < 0 or port > 65535:
                        raise Exception('Port is not valid')

                endpoint: re.Match = re.match('\w', ip_split[1])
                if not endpoint:
                    raise Exception('wut it is?')

        return True

    def __set_ip_data_source(self, local_address: str):
        protocol: str = ''
        for working_protocol in self.__working_protocols:
            if working_protocol in local_address:
                protocol = working_protocol
                break

        if protocol:
            local_address: str = local_address.replace(f'{protocol}://', '')
        else:
            protocol: str = 'http'
        if self.__verify_ip(local_address):
            self.__data_source = f'{protocol}://{local_address}'
