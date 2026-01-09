from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4
import enum


if TYPE_CHECKING:
    from .user import User


class ThemeOption(str, enum.Enum):
    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"


class DashboardLayout(str, enum.Enum):
    DEFAULT = "default"
    COMPACT = "compact"
    FOCUS = "focus"


class UserPreferencesBase(SQLModel):
    theme: ThemeOption = Field(default=ThemeOption.LIGHT)
    language: str = Field(default="en", max_length=10)
    timezone: str = Field(default="UTC", max_length=50)
    notifications_enabled: bool = Field(default=True)
    dashboard_layout: DashboardLayout = Field(default=DashboardLayout.DEFAULT)


class UserPreferences(UserPreferencesBase, table=True):
    __tablename__ = "user_preferences"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", unique=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)

    # Relationship to user
    user: "User" = Relationship(back_populates="preferences")