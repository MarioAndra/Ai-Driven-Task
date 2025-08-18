from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class TimeStampedModel(SQLModel, table=False):
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, nullable=False)
