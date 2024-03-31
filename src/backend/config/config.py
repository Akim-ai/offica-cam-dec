from os import environ

SERVER_SECRET_TOKEN = environ.get('./././envs/api.env')
JWT_ACCESS_TOKEN_EXP_TIME = 3600

