import asyncio
from os import environ

from dotenv import load_dotenv

from src.Database.Main.DB import DBSession, DBEngine
from src.Database.Main.base import Base
from src.Database.Main.config.dbConfig import DBConfig
from app import app


def get_all_routes(app):
    url_list = []
    for route in app.router.routes_all.values():
        if route.methods != {'OPTIONS'}:  # Exclude automatic OPTIONS routes
            methods = ','.join(route.methods)
            url_list.append(f"{methods} {route.path}")
    return url_list



def run_backend_server():
    routes = get_all_routes(app)
    for route in routes:
        print(route)
    app.run(host="127.0.0.1", port=8000, debug=True, auto_reload=True, workers=4)


def run_main_db():
    load_dotenv('envs/api.env')
    config = DBConfig(connection_string=environ.get('MAIN_DB_CONNECTION_STRING'))
    async def _run():
        session = await DBSession().get_session
        print(session, type(session))
        async with session() as ss:
            # async with ss.begin():
            #     test_user = AnonymousUser()
            #     test_user.id = uuid.uuid4()
                # ss.add(test_user)
            print(2131)
            # stmt = select(AnonymousUser.id).where(AnonymousUser.id == '123')
            # test = await ss.execute(stmt)
            # for i in test:
            #     print(i)

    async def drop_all():

        engine = DBEngine().engine
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def create_all():
        engine = DBEngine().engine
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(create_all())
    # asyncio.run(create_test_user_with_auth())


if __name__ == '__main__':
    run_backend_server()
    # run_main_db()
