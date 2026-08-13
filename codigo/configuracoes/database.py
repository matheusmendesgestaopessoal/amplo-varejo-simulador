import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_DW_DATABASE = os.getenv("MYSQL_DW_DATABASE")

def conectar_mysql():

    url = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    )

    return create_engine(url)

def conectar_dw():

    url = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DW_DATABASE}"
    )

    return create_engine(url)

