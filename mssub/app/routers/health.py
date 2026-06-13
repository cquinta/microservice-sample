import logging

from fastapi import APIRouter
from pydantic import BaseModel

logger = logging.getLogger("fastapi-service-sub")

router = APIRouter()




@router.get("/health")
async def health():
    logger.info(f" status: healthy")
    return {"status": "healthy"}
