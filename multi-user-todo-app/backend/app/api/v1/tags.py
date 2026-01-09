from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from app.database.session import get_session
from app.models.user import User
from app.models.tag import Tag, TagCreate, TagUpdate
from app.services.tag_service import get_tags, get_tag_by_id, create_tag, update_tag, delete_tag
from app.utils.dependencies import get_current_user
from app.schemas.tag import TagResponse

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/", response_model=List[TagResponse])
def read_tags(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    tags = get_tags(session=session, user_id=current_user.id)
    return tags


@router.post("/", response_model=TagResponse)
def create_tag_item(
    tag: TagCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    db_tag = create_tag(
        session=session,
        tag_create=tag,
        user_id=current_user.id
    )
    return db_tag


@router.get("/{tag_id}", response_model=TagResponse)
def read_tag(
    tag_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    from uuid import UUID
    try:
        tag_uuid = UUID(tag_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid tag ID format")
    
    db_tag = get_tag_by_id(session=session, tag_id=tag_uuid, user_id=current_user.id)
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag


@router.put("/{tag_id}", response_model=TagResponse)
def update_tag_item(
    tag_id: str,
    tag_update: TagUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    from uuid import UUID
    try:
        tag_uuid = UUID(tag_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid tag ID format")
    
    db_tag = update_tag(
        session=session,
        tag_id=tag_uuid,
        tag_update=tag_update,
        user_id=current_user.id
    )
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag


@router.delete("/{tag_id}")
def delete_tag_item(
    tag_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    from uuid import UUID
    try:
        tag_uuid = UUID(tag_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid tag ID format")
    
    success = delete_tag(session=session, tag_id=tag_uuid, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"message": "Tag deleted successfully"}