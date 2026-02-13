from pydantic import BaseModel, Field
from typing import List, Optional


class EventIn(BaseModel):
    user_id: str
    item_id: str
    event_type: str = Field(description="expose|click|play|finish|like|favorite")
    ts: int


class FeedItem(BaseModel):
    item_id: str
    score: float
    sources: List[str]


class FeedResponse(BaseModel):
    user_id: str
    scene: str
    size: int
    items: List[FeedItem]
    debug: Optional[dict] = None
