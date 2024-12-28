from dataclasses import dataclass


@dataclass(slots=True)
class RefreshDTO:
    refresh_token: str


@dataclass(slots=True)
class RefreshResponseDTO:
    access_token: str
