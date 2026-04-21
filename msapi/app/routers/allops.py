import asyncio

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class CalcInput(BaseModel):
    a: int
    b: int

import os

SUM_SERVICE_URL = os.getenv("SUM_SERVICE_URL", "http://mssum:80/sum")
SUB_SERVICE_URL = os.getenv("SUB_SERVICE_URL", "http://mssub:80/sub")


async def call_microservice(url: str, payload: dict) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        return response.json()


@router.post("/allops")
async def calculate_all(data: CalcInput):
    payload = {"a": data.a, "b": data.b}

    try:
        sum_task, sub_task = await asyncio.gather(
            call_microservice(SUM_SERVICE_URL, payload),
            call_microservice(SUB_SERVICE_URL, payload),
        )

        return {
            "input": payload,
            "results": {
                "sum_service": sum_task,
                "sub_service": sub_task,
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
