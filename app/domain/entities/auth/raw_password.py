from dataclasses import dataclass

from app.domain.exception import DomainFieldError


@dataclass(frozen=True, slots=True)
class RawPassword:
    MIN_LEN = 6

    password: str

    def __post_init__(self) -> None:
        self.__validate_password_length()

    def __validate_password_length(self) -> None:
        if len(self.password) < self.MIN_LEN:
            raise DomainFieldError(
                f'Password must be at least {self.MIN_LEN} characters long.',
            )
