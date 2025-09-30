from dataclasses import dataclass
from datetime import datetime


@dataclass
class RefreshTokenDM:
    token: str
    username: str
    expires_at: datetime
    revoked: bool = False
