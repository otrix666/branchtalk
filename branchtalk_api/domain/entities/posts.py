from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Post:
    id: int | None
    content: str
    user_id: int
    created_at: datetime
    updated_at: datetime
