from dataclasses import dataclass


@dataclass(slots=True)
class UserCreateDTO:
    username: str
    email: str
    password: str


@dataclass(slots=True)
class UserLoginDTO:
    username: str
    password: str


@dataclass(slots=True)
class LoginResponseDTO:
    access_token: str
    refresh_token: str
