from fastapi import FastAPI
from src.auth.router import router as auth_router
from src.letter.router import router as letter_router

app = FastAPI()


app.include_router(auth_router, prefix="/auth")
app.include_router(letter_router, prefix="/letter")


@app.get("/")
async def root():
    return {"message": "Hello World"}
