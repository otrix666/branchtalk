from pydantic import BaseModel

from branchtalk_api.application.dto.refresh import RefreshDTO


class RefreshToken(BaseModel):
    refresh_token: str

    def to_dto(self) -> RefreshDTO:
        return RefreshDTO(
            refresh_token=self.refresh_token,
        )
