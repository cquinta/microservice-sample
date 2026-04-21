from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class CalcInput(BaseModel):
    a: int
    b: int


@router.post("/sub")
async def calc_sum(data: CalcInput):
    result = data.a - data.b 
    return {"result": result, "op":"sub"}

