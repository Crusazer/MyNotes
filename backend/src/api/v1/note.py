import uuid
from typing import Annotated

from fastapi import APIRouter, Body, Path
from fastapi.params import Depends
from starlette import status
from starlette.responses import JSONResponse

from src.core.database.models.user import User
from src.core.dependencies import get_current_active_user, get_note_service
from src.core.schemas.note import SNote, SNoteCreate, SNoteEdit
from src.services.note import NoteService

router = APIRouter(prefix="/notes", tags=["note"])


@router.get("/all/", response_model=list[SNote])
async def get_all_notes(
    user: User = Depends(get_current_active_user),
    note_service: NoteService = Depends(get_note_service),
) -> list[SNote]:
    return await note_service.get_all_notes(user)


@router.post("/create/", response_model=SNote, status_code=status.HTTP_201_CREATED)
async def create_note(
    note: Annotated[SNoteCreate, Body()],
    user: User = Depends(get_current_active_user),
    note_service: NoteService = Depends(get_note_service),
):
    return await note_service.create_note(user, note)


@router.delete("/delete/{note}/", status_code=status.HTTP_202_ACCEPTED)
async def delete_note(
    note: Annotated[uuid.UUID, Path()],
    user: User = Depends(get_current_active_user),
    note_service: NoteService = Depends(get_note_service),
) -> JSONResponse:
    await note_service.delete_note(user, note)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"message": "Note deleted."}
    )


@router.patch(
    "/update/{note_uuid}", response_model=SNote, status_code=status.HTTP_200_OK
)
async def update_note(
    note_uuid: Annotated[uuid.UUID, Path()],
    note: Annotated[SNoteEdit, Body()],
    user: User = Depends(get_current_active_user),
    note_service: NoteService = Depends(get_note_service),
) -> SNote:
    return await note_service.edit_note(user, note_uuid, note)
