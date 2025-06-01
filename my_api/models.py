from sqlalchemy import Table, Column, Integer, String, Float, MetaData

metadata = MetaData()


Item = Table(
    "item",
    metadata,
    Column("id", Integer, primary_key=True),
    
    Column("name", String),
    
    Column("price", Float),
    
)

User = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    
    Column("username", String),
    
    Column("email", String),
    
)
