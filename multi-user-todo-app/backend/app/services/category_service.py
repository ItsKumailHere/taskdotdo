from sqlmodel import Session, select
from typing import List, Optional
from app.models.category import Category, CategoryCreate, CategoryUpdate
from fastapi import HTTPException, status
import uuid


def get_categories(session: Session, user_id: uuid.UUID) -> List[Category]:
    return session.exec(
        select(Category).where(Category.user_id == user_id)
    ).all()


def get_category_by_id(session: Session, category_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Category]:
    return session.exec(
        select(Category).where(
            Category.id == category_id,
            Category.user_id == user_id
        )
    ).first()


def create_category(session: Session, category_create: CategoryCreate, user_id: uuid.UUID) -> Category:
    # Check if category name already exists for this user
    existing_category = session.exec(
        select(Category).where(
            Category.name == category_create.name,
            Category.user_id == user_id
        )
    ).first()
    
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists for this user"
        )
    
    db_category = Category(
        name=category_create.name,
        user_id=user_id
    )
    
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    
    return db_category


def update_category(session: Session, category_id: uuid.UUID, category_update: CategoryUpdate, user_id: uuid.UUID) -> Optional[Category]:
    db_category = session.exec(
        select(Category).where(
            Category.id == category_id,
            Category.user_id == user_id
        )
    ).first()
    
    if not db_category:
        return None
    
    if category_update.name is not None:
        # Check if new name already exists for this user
        existing_category = session.exec(
            select(Category).where(
                Category.name == category_update.name,
                Category.user_id == user_id,
                Category.id != category_id
            )
        ).first()
        
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name already exists for this user"
            )
        
        db_category.name = category_update.name
    
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    
    return db_category


def delete_category(session: Session, category_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    db_category = session.exec(
        select(Category).where(
            Category.id == category_id,
            Category.user_id == user_id
        )
    ).first()
    
    if not db_category:
        return False
    
    session.delete(db_category)
    session.commit()
    return True