from pydantic import BaseModel
from typing import Optional
from sqlmodel import Field
from ..models.user_preferences import ThemeOption, DashboardLayout


class UserPreferencesBase(BaseModel):
    theme: ThemeOption = ThemeOption.LIGHT
    language: str = "en"
    timezone: str = "UTC"
    notifications_enabled: bool = True
    dashboard_layout: DashboardLayout = DashboardLayout.DEFAULT


class UserPreferencesCreate(UserPreferencesBase):
    pass


class UserPreferencesRead(UserPreferencesBase):
    id: str
    user_id: str
    created_at: str
    updated_at: Optional[str] = None


class UserPreferencesUpdate(BaseModel):
    theme: Optional[ThemeOption] = None
    language: Optional[str] = None
    timezone: Optional[str] = None
    notifications_enabled: Optional[bool] = None
    dashboard_layout: Optional[DashboardLayout] = None