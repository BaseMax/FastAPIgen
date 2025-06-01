from sqlalchemy import Table, Column, Integer, String, Float

metadata = MetaData()


Item = Table(
    "item",
    metadata,
    Column("id", Integer, primary_key=True),
    
    Column("name", Str),
    
    Column("price", Float),
    
)
