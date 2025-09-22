from dataclasses import dataclass


@dataclass(eq=False)
class ApplicationError(Exception):
    @property
    def message(self) -> str:
        return "Application error"


@dataclass(eq=False)
class EntityAlreadyExistsError(ApplicationError):
    @property
    def message(self) -> str:
        return "Entity already exists"


@dataclass(eq=False)
class EntityNotExistsError(ApplicationError):
    def __init__(self, message: str = "Entity doesn't exists") -> None:
        self.msg = message

    @property
    def message(self) -> str:
        return self.msg
