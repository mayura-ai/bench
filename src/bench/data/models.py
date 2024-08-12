from pydantic import BaseModel, Field
from typing import List, Optional
import datetime
import uuid


class Metadata(BaseModel):
    date: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    website: str
    exam: str
    url: str


class Content(BaseModel):
    is_multimodal: bool
    question: str
    options: List[dict]
    images: Optional[List[str]] = None
    correct_label: Optional[str] = None


class DataItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    metadata: Metadata
    content: Content
