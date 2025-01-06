from pydantic import BaseModel

from branchtalk_api.application.dto.user import RefreshDTO, UserCreateDTO, UserLoginDTO


class UserLogin(BaseModel):
    username: str
    password: str

    def to_dto(self) -> UserLoginDTO:
        return UserLoginDTO(
            username=self.username,
            password=self.password,
        )


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    def to_dto(self) -> UserCreateDTO:
        return UserCreateDTO(
            username=self.username,
            email=self.email,
            password=self.password,
        )


class RefreshToken(BaseModel):
    refresh_token: str

    def to_dto(self) -> RefreshDTO:
        return RefreshDTO(
            refresh_token=self.refresh_token,
        )
