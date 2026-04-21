from fastapi import Depends, FastAPI

from .routers import sum

app = FastAPI(tittle="Sum Microsservice")

app.include_router(sum.router)

@app.get("/")
async def root():
    return {"message": "Microsserviço de Soma"}
