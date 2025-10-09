from dataclasses import dataclass
from typing import TypedDict


class JwtPayload(TypedDict):
    token: str
    exp: float


@dataclass
class Jwt:
    payload: JwtPayload
    secret: str
    algorithm: str
