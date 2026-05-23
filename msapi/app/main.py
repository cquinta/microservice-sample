from fastapi import FastAPI

from .routers import allops
from .routers import version
import os

app = FastAPI(tittle="Cal  Microsservice")

app.include_router(allops.router)
app.include_router(version.router)

@app.get("/")
async def root():
    return {"message": "Microsserviço de Cálculos", "host": os.getenv("HOSTNAME")}
