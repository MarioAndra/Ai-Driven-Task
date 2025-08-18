from typing import Optional
from sqlmodel import Field
from .base import TimeStampedModel

class Admin(TimeStampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True)
    password: str
    role: str = Field(default="admin")
