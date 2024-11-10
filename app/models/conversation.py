from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    summary: str
    avg_sentiment: str
    ai_suggestions: str
    created_at: datetime = Field(default=datetime.now())
