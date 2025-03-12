from fastapi import FastAPI
from .routers.auth.auth import router as auth_router
from .db.database import engine
from sqlalchemy.ext.asyncio import async_sessionmaker
app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["users"])

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit = False)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
