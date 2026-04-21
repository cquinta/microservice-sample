from fastapi import FastAPI

from .routers import allops

app = FastAPI(tittle="Cal  Microsservice")

app.include_router(allops.router)

@app.get("/")
async def root():
    return {"message": "Microsserviço de Cálculos"}
