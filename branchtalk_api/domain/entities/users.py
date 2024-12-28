from dataclasses import dataclass


@dataclass(slots=True)
class User:
    id: int | None
    username: str
    email: str
    password: str
