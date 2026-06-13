from fastapi import FastAPI
from .config import Config
from .routers import allops
from .routers import health

import os

app = FastAPI(tittle="Cal  Microsservice")

app.include_router(allops.router)
app.include_router(health.router)



@app.get("/")
async def root():
    return {"message": "Microsserviço de Cálculos", "host": Config.HOST, "version": Config.VERSION}
