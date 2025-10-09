from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, registry

mapper_registry = registry(metadata=MetaData())


class BaseModel(DeclarativeBase):
    registry = mapper_registry
    metadata = mapper_registry.metadata
