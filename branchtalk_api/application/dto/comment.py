from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class CreateCommentDTO:
    content: str
    created_at: datetime
    updated_at: datetime
    user_id: int
    post_id: int
    parent_comment_id: int | None


@dataclass(slots=True)
class UpdateCommentDTO:
    comment_id: int
    content: str
    updated_at: datetime
    user_id: int


@dataclass(slots=True)
class DeleteCommentDTO:
    comment_id: int
    user_id: int
