# Models package
from . import user, todo  # noqa: F401

# Import all models to register them with SQLModel
from .user import User  # noqa: F401
from .todo import Todo  # noqa: F401
