"""
Todo-related schemas
"""
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from ..models.base import TodoBase, TodoCreate, TodoUpdate, TodoPublic