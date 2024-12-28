from datetime import datetime

from pydantic import BaseModel

from branchtalk_api.application.dto.comment import CreateCommentDTO, DeleteCommentDTO, UpdateCommentDTO


class CreateComment(BaseModel):
    content: str
    created_at: datetime
    updated_at: datetime
    user_id: int
    post_id: int
    parent_comment_id: int | None

    def to_dto(self) -> CreateCommentDTO:
        return CreateCommentDTO(
            content=self.content,
            created_at=self.created_at,
            updated_at=self.updated_at,
            user_id=self.user_id,
            post_id=self.post_id,
            parent_comment_id=self.parent_comment_id,
        )


class UpdateComment(BaseModel):
    comment_id: int
    content: str
    updated_at: datetime
    user_id: int

    def to_dto(self) -> UpdateCommentDTO:
        return UpdateCommentDTO(
            comment_id=self.comment_id,
            content=self.content,
            updated_at=self.updated_at,
            user_id=self.user_id,
        )


class DeleteComment(BaseModel):
    comment_id: int
    user_id: int

    def to_dto(self):
        return DeleteCommentDTO(
            comment_id=self.comment_id,
            user_id=self.user_id,
        )
