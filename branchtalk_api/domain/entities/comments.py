from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Comment:
    id: int | None
    content: str
    created_at: datetime
    updated_at: datetime
    user_id: int
    post_id: int
    parent_comment_id: int | None
