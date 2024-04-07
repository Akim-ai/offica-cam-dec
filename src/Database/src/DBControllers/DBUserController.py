import hashlib
import os
import uuid
from pprint import pprint

import aiofiles
from aiofiles.os import remove
from pydantic import NonNegativeInt
from sqlalchemy import select, Result, Row, text
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


from src.Database.Loggers import UserLogger
from src.Database.Models.User import User
from src.Database.src.DBControllers.Abstract.SessionManager import SessionManager
from src.shared.datatypes.api.Pagination import Paginator
from src.shared.datatypes.api.UserViewType import AuthLoginData
from src.shared.datatypes.db.IUser import IUser, IUserWithImage, IListUserWithImage
from src.Database.src.Writers.utils.recursive_path_creator import recursive_folder_creator


user_assigner_no_password = lambda user: IUser(
    id=user[0], first_name=user[1],
    last_name=user[1], detected_path_image=user[3]
)


class DBUserController(SessionManager):

    session: async_sessionmaker[AsyncSession]
    __logger = UserLogger
    __offset: int = 20
    __limit: int = 20

    __save_path: str = 'users_detected'

    @staticmethod
    def hash_password(password: str):
        hash_object = hashlib.sha512()

        # Encode the password to bytes and hash it
        hash_object.update(password.encode('utf-8'))

        # Return the hexadecimal representation of the hash
        return hash_object.hexdigest()

    async def get_all_detected_users(self):
        try:
            users_result = IListUserWithImage()
            async with self.session() as conn:
                users = await conn.execute(select(User).where(User.is_disabled == False and User.detected_path_image))
                all_users = users.all()
                if all_users:
                    all_users = all_users[0]
                self.__logger.log('debug', message='all detected users -> gotten')
                path = os.getcwd()
                for user in all_users:
                    user: User
                    async with aiofiles.open(f'{path}/static/{user.detected_path_image}', 'rb') as out_file:
                        image = await out_file.read()
                    users_result.users.append(IUserWithImage(
                        id=user.id, first_name=user.first_name,
                        last_name=user.last_name, detected_path_image=user.detected_path_image,
                        detected_image=image.hex(),
                    ))

            return users_result.model_dump_json()

        except Exception as e:
            pprint(e)

    async def get_user(self, user_id: int):
        raw_user = """
        SELECT *
        FROM "user" 
        WHERE id=:user_id AND is_disabled = False
        """
        async with self.session() as conn:
            conn: AsyncSession
            result_user: Result = await conn.execute(text(raw_user), {'user_id': user_id})
            result_user: Row = result_user.first()
            if not result_user:
                return {'error': "Doesn't exists"}
            print(result_user)
            user: IUser = user_assigner_no_password(result_user)
            return user.model_dump(exclude={"password": True})

    async def get_paginated_user(self, page: NonNegativeInt):
        raw_users = """
        SELECT id, first_name, last_name, detected_path_image
        FROM "user" 
        WHERE "user".is_disabled = FALSE
        OFFSET :offset LIMIT :limit
        """

        raw_cnt_users = """
        SELECT COUNT(*)
        FROM "user"
        WHERE is_disabled = FALSE
        """
        async with self.session() as conn:
            conn: AsyncSession
            result_users: Result = await conn.execute(
                text(raw_users),
                {'offset': self.__offset * (page - 1), 'limit': self.__limit}
            )

            result_cnt = await conn.execute(text(raw_cnt_users))
            cnt = result_cnt.fetchall()
            if not cnt:
                return {'error': "Doesn't exists"}

            result_pagination: dict = Paginator.assign(
                objects=result_users,
                assigner=user_assigner_no_password,
                cnt=cnt[0][0],
                offset=self.__offset,
                page=page,
                excluded={'password'}
            )
            return result_pagination


    async def create_user(self, data: IUserWithImage):
        user: User = User(first_name=data.first_name, last_name=data.last_name)
        if data.password:
            user.set_password(data.password)
        if data.username:
            user.username = data.username
        
        raw_user_select = """
                            SELECT id
                            FROM "user"
                            WHERE first_name = :first_name and
                            last_name = :last_name AND
                            detected_path_image = :detected_image
                         """

        path_with_image: str = f'static/{self.__save_path}/{uuid.uuid4()}.jpg'
        async with self.session() as conn:
            conn: AsyncSession
            user.detected_path_image = path_with_image
            conn.add(user)
            await conn.commit()
            created_user: Result = await conn.execute(
                    text(raw_user_select), 
                    {
                        "first_name": data.first_name,
                        "last_name": data.last_name,
                        "detected_image": path_with_image,
                    })
            created_user_first: Row = created_user.first()
            if not created_user_first:
                return ''
            user_id: int = created_user_first[0]
            print(user_id)
            self.__logger.log('debug', message='user -> created')

        cwd = os.getcwd()
        path = cwd + self.__save_path
        if not os.path.exists(path=path):
            recursive_folder_creator(path=path)
        async with aiofiles.open(f'{cwd}/{path_with_image}', 'wb') as out_file:
            await out_file.write(data.detected_image)
            self.__logger.log('debug', message='user id frame -> written')
        print('created')
        user: dict = IUser(
                id=user_id, first_name=data.first_name, 
                last_name=data.last_name,
                detected_path_image=path_with_image,
                username=data.username
                ).model_dump(exclude=["password"])
        return user

    async def delete_user(self, user_id: int):

        raw_user_delete = """
        UPDATE "user"
        SET is_disabled = True
        WHERE id = :user_id and
        is_disabled = FALSE
        """

        raw_user_get = """
        SELECT detected_path_image
        FROM "user"
        WHERE id = :user_id AND is_disabled = True
        """

        async with self.session() as conn:
            result = await conn.execute(
                text(raw_user_delete),
                {'user_id': user_id}
            )
            print(result)

            user = await conn.execute(
                text(raw_user_get),
                {'user_id': user_id}
            )
            user = user.first()
            if not user:
                return 400
            print(user)
            file_path = os.path.join(os.getcwd(), self.__save_path, user.detected_path_image)
            await conn.commit()
            try:
                self.__logger.log('debug', message=f"File {file_path} successfully deleted.")
            except FileNotFoundError:
                self.__logger.log('debug', f"File {file_path} not found.")
                return 200
            except Exception as e:
                self.__logger.log('debug', message=f"Error deleting file {file_path}: {e}")
                return 410
        return 200

    async def get_auth_user(self, data: AuthLoginData):
        raw_select = """
        SELECT id, first_name, last_name,
        detected_path_image, username, password
        FROM "user"
        WHERE is_disabled = FALSE AND
        password = :password AND
        username = :username 
        """
        
        async with self.session() as conn:
            conn: AsyncSession
            result = await conn.execute(text(raw_select), {
                'password': User.hash_password(data.password),
                'username': data.username
            })
            user = result.first()
            if not user:
                return {'error': 'Invalid credentials'}
            print(user)
            if self.hash_password(data.password) != user[5]:
                return {"error": "Invalid credentials"}

            return IUser(
                id=user[0],
                first_name=user[1],
                last_name=user[2],
                detected_path_image=user[3],
                username=user[4]
            ).model_dump(exclude=["password"])

