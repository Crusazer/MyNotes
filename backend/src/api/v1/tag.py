from typing import Annotated

from fastapi import APIRouter, Body, Depends
from starlette import status
from starlette.responses import JSONResponse

from src.core.database.models.user import User
from src.core.dependencies import get_tag_service, get_current_active_user
from src.core.schemas.tag import STag
from src.services.tag_service import TagService

router = APIRouter(prefix="/tags", tags=["tag"])


@router.post("/create/", status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_name: Annotated[str, Body()],
    tag_service: TagService = Depends(get_tag_service),
    user: User = Depends(get_current_active_user),
):
    await tag_service.create_tag(tag_name)
    return JSONResponse({"message": "Successfully created."})


@router.get("/all/", response_model=list[STag])
async def get_all_tags(
    user: User = Depends(get_current_active_user),
    tag_service: TagService = Depends(get_tag_service),
) -> list[STag]:
    return await tag_service.get_all_tags()
