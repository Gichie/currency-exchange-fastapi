from fastapi import APIRouter
from starlette.responses import FileResponse

router = APIRouter()


@router.get("/", tags=["Root"])
async def root():
    return FileResponse("src/static/templates/index.html")
