
from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    text: str
    lang: str = 'auto'
    channel: str = 'text'

class ChatResponse(BaseModel):
    answer: str
    citations: List[str]
    redacted_query: str
    consent_id: str
    confidence: float

class KBItem(BaseModel):
    text: str
    source: Optional[str] = None
