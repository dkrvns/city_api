from dataclasses import dataclass
from typing import TypedDict


class JwtPayload(TypedDict):
    token: str
    expires_in: float


@dataclass
class Jwt:
    payload: JwtPayload
    secret: str
    algorithm: str
