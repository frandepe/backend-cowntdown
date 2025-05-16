from fastapi import FastAPI
from routes.user import user
from routes.animal import animal

app = FastAPI()

# Agregamos las rutas de cada módulo y nombre para la documentacion asd
app.include_router(user, prefix="/users", tags=["Users"])
app.include_router(animal, prefix="/animals",tags=["Animals"])

@app.get("/")
def read_root():
    return {"Hello": "World"}


