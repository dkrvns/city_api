import uuid
from dataclasses import dataclass


@dataclass
class UserDM:
    id: uuid.UUID
    email: str
    hashed_password: bytes
