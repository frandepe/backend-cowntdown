from fastapi import FastAPI
from routes.user import user

app = FastAPI()
# Include the user router with a prefix
app.include_router(user, prefix="/users", tags=["Users"])

@app.get("/")
def read_root():
    return {"Hello": "World"}