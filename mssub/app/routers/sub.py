import logging

from fastapi import APIRouter
from pydantic import BaseModel

logger = logging.getLogger("fastapi-service-sub")

router = APIRouter()


class CalcInput(BaseModel):
    a: int
    b: int


@router.post("/sub")
async def calc_sum(data: CalcInput):
    result = data.a - data.b
    logger.info(f"Subtraction: {data.a} - {data.b} = {result}")
    return {"result": result, "op": "sub"}
