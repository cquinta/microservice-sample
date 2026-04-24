from fastapi import Depends, FastAPI

from .routers import sub

app = FastAPI(title="Sub Microsservice")

app.include_router(sub.router)

@app.get("/")
async def root():
    return {"message": "Microsserviço de Subtração"}
