import asyncio

import httpx
from fastapi import APIRouter, HTTPException

router = APIRouter()


import os

@router.get("/version")
async def call_version() -> str:
    return os.getenv("VERSION")
