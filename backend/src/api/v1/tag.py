from typing import Annotated

from fastapi import APIRouter, Body, Depends
from src.core.database.models.user import User
from src.core.dependencies import get_tag_service, get_current_active_user
from src.core.schemas.tag import STag, STagGet
from src.services.tag_service import TagService
from starlette import status
from starlette.responses import JSONResponse

router = APIRouter(prefix="/v1/tags", tags=["tag"])


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


@router.delete("/delete/", status_code=status.HTTP_202_ACCEPTED)
async def delete_tag(
    s_tag: Annotated[STagGet, Body()],
    user: User = Depends(get_current_active_user),
    tag_service: TagService = Depends(get_tag_service),
) -> JSONResponse:
    await tag_service.delete_tag(s_tag)
    return JSONResponse({"message": "Successfully deleted."})
