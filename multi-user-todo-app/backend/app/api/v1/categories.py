from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from app.database.session import get_session
from app.models.user import User
from app.models.category import Category, CategoryCreate, CategoryUpdate
from app.services.category_service import get_categories, get_category_by_id, create_category, update_category, delete_category
from app.utils.dependencies import get_current_user
from app.schemas.category import CategoryResponse

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=List[CategoryResponse])
def read_categories(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    categories = get_categories(session=session, user_id=current_user.id)
    return categories


@router.post("/", response_model=CategoryResponse)
def create_category_item(
    category: CategoryCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    db_category = create_category(
        session=session,
        category_create=category,
        user_id=current_user.id
    )
    return db_category


@router.get("/{category_id}", response_model=CategoryResponse)
def read_category(
    category_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    from uuid import UUID
    try:
        category_uuid = UUID(category_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid category ID format")
    
    db_category = get_category_by_id(session=session, category_id=category_uuid, user_id=current_user.id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category_item(
    category_id: str,
    category_update: CategoryUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    from uuid import UUID
    try:
        category_uuid = UUID(category_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid category ID format")
    
    db_category = update_category(
        session=session,
        category_id=category_uuid,
        category_update=category_update,
        user_id=current_user.id
    )
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.delete("/{category_id}")
def delete_category_item(
    category_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    from uuid import UUID
    try:
        category_uuid = UUID(category_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid category ID format")
    
    success = delete_category(session=session, category_id=category_uuid, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}