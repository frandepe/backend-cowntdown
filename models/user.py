from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta, engine

users = Table(
    "users",
    meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
    Column("email", String(255)),
    Column("password", String(255)),
)
# Con meta le decimos, una vez conectado a mysql quiero que crees esa tabla de arriba
meta.create_all(engine)
