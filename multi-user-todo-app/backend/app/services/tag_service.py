from sqlmodel import Session, select
from typing import List, Optional
from app.models.tag import Tag, TagCreate, TagUpdate
from fastapi import HTTPException, status
import uuid


def get_tags(session: Session, user_id: uuid.UUID) -> List[Tag]:
    return session.exec(
        select(Tag).where(Tag.user_id == user_id)
    ).all()


def get_tag_by_id(session: Session, tag_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Tag]:
    return session.exec(
        select(Tag).where(
            Tag.id == tag_id,
            Tag.user_id == user_id
        )
    ).first()


def create_tag(session: Session, tag_create: TagCreate, user_id: uuid.UUID) -> Tag:
    # Check if tag name already exists for this user
    existing_tag = session.exec(
        select(Tag).where(
            Tag.name == tag_create.name,
            Tag.user_id == user_id
        )
    ).first()
    
    if existing_tag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag with this name already exists for this user"
        )
    
    db_tag = Tag(
        name=tag_create.name,
        user_id=user_id
    )
    
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)
    
    return db_tag


def update_tag(session: Session, tag_id: uuid.UUID, tag_update: TagUpdate, user_id: uuid.UUID) -> Optional[Tag]:
    db_tag = session.exec(
        select(Tag).where(
            Tag.id == tag_id,
            Tag.user_id == user_id
        )
    ).first()
    
    if not db_tag:
        return None
    
    if tag_update.name is not None:
        # Check if new name already exists for this user
        existing_tag = session.exec(
            select(Tag).where(
                Tag.name == tag_update.name,
                Tag.user_id == user_id,
                Tag.id != tag_id
            )
        ).first()
        
        if existing_tag:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tag with this name already exists for this user"
            )
        
        db_tag.name = tag_update.name
    
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)
    
    return db_tag


def delete_tag(session: Session, tag_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    db_tag = session.exec(
        select(Tag).where(
            Tag.id == tag_id,
            Tag.user_id == user_id
        )
    ).first()
    
    if not db_tag:
        return False
    
    session.delete(db_tag)
    session.commit()
    return True