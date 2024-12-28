from datetime import datetime

from pydantic import BaseModel

from branchtalk_api.application.dto.post import CreatePostDTO, DeletePostDTO, UpdatePostDTO


class CreatePost(BaseModel):
    content: str
    user_id: int
    created_at: datetime
    updated_at: datetime

    def to_dto(self) -> CreatePostDTO:
        return CreatePostDTO(
            content=self.content,
            user_id=self.user_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class UpdatePost(BaseModel):
    post_id: int
    content: str
    user_id: int
    updated_at: datetime

    def to_dto(self) -> UpdatePostDTO:
        return UpdatePostDTO(
            post_id=self.post_id,
            content=self.content,
            user_id=self.user_id,
            updated_at=self.updated_at,
        )


class DeletePost(BaseModel):
    post_id: int
    user_id: int

    def to_dto(self):
        return DeletePostDTO(
            post_id=self.post_id,
            user_id=self.user_id,
        )
