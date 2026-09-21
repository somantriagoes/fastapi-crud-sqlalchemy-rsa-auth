import os

from sqlalchemy import MetaData, create_engine

from dotenv import load_dotenv

load_dotenv()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")
port = os.getenv("DB_PORT")

DATABASE_URL = (
    f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
)

engine = create_engine(DATABASE_URL)
meta = MetaData()
conn = engine.connect()

