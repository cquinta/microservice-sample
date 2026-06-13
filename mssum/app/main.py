from fastapi import Depends, FastAPI

from .routers import sum
from .routers import health


app = FastAPI(tittle="Sum Microsservice")

app.include_router(sum.router)
app.include_router(health.router)

@app.get("/")
async def root():
    return {"message": "Microsserviço de Soma"}
