from fastapi import FastAPI

santa_app = FastAPI()


@santa_app.get("/")
async def root():
    return {"message": "Ho ho ho! Merry XMas!"}
