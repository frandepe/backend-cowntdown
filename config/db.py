from sqlalchemy import create_engine, MetaData

# create_engine = create_engine("mysql+pymysql://root:password@localhost:3306/fastapi") # Esto si tuvieras una contraseña
# mysql+pymysql://root:password@containers-us-west-17.railway.app:6414/fastapi #Ejemplo de una base de datos en Railway

engine = create_engine("mysql+pymysql://root:@localhost:3306/fastapi")
meta = MetaData()

conn = engine.connect()
