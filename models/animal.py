from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import String, Integer, Boolean
from config.db import meta, engine


animals = Table(
    "animals",
    meta,
    Column("id", Integer, primary_key=True, autoincrement=True ),
    Column("Kind", String(30)),
    Column("Weight", String(30)),
    Column("Height", String(30)),
    Column("IsInSale", Boolean),
)

meta.create_all(engine)