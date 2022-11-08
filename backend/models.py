"""SQLAlchemy database models"""
from sqlalchemy import DATE, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text

from .database import Base


class Todo(Base):
    __tablename__ = "todo"
    todo_id = Column(Integer, primary_key=True, nullable=False)
    todo_name = Column(String, nullable=False)
    level_of_importance = Column(String, nullable=False)
    date_ceated = Column(DATE(), nullable=False, server_default=func.now())
