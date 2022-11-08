from datetime import date

from pydantic import BaseModel, root_validator

from .validators import validate_level_of_importance


class TodoCreate(BaseModel):
    todo_name: str
    level_of_importance: str
    _level_of_importance_validator = root_validator(allow_reuse=True)(
        validate_level_of_importance
    )


class TodoResponse(BaseModel):
    todo_id: int
    todo_name: str
    level_of_importance: str
    date_created: date
