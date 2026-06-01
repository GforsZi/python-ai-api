from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from . import service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/github")
async def github_login():
    url = service.get_github_auth_url()
    return RedirectResponse(url)


@router.get("/callback")
async def github_callback(code: str, db: AsyncSession = Depends(get_db)):
    result = await service.github_login(db, code)
    return JSONResponse(content=result, status_code=result["status_code"])
