from fastapi import FastAPI
from .routers.auth.auth import router as auth_router
app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
