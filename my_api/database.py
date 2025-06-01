from databases import Database
from sqlalchemy import create_engine, MetaData
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///mydb.db")

database = Database(DATABASE_URL)
metadata = MetaData()

# Import models to register them with metadata
from models import Item, User