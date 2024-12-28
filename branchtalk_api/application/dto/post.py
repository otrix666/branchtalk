from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class CreatePostDTO:
    content: str
    created_at: datetime
    updated_at: datetime
    user_id: int


@dataclass(slots=True)
class UpdatePostDTO:
    post_id: int
    content: str
    user_id: int
    updated_at: datetime


@dataclass(slots=True)
class DeletePostDTO:
    post_id: int
    user_id: int
