from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class Region(_message.Message):
    __slots__ = ("id", "name", "capital")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CAPITAL_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    capital: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., capital: _Optional[str] = ...) -> None: ...

class NewRegionDTO(_message.Message):
    __slots__ = ("name", "capital")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CAPITAL_FIELD_NUMBER: _ClassVar[int]
    name: str
    capital: str
    def __init__(self, name: _Optional[str] = ..., capital: _Optional[str] = ...) -> None: ...

class RegionIdRequest(_message.Message):
    __slots__ = ("region_id",)
    REGION_ID_FIELD_NUMBER: _ClassVar[int]
    region_id: str
    def __init__(self, region_id: _Optional[str] = ...) -> None: ...

class RegionIdResponse(_message.Message):
    __slots__ = ("region_id",)
    REGION_ID_FIELD_NUMBER: _ClassVar[int]
    region_id: str
    def __init__(self, region_id: _Optional[str] = ...) -> None: ...

class RegionList(_message.Message):
    __slots__ = ("regions",)
    REGIONS_FIELD_NUMBER: _ClassVar[int]
    regions: _containers.RepeatedCompositeFieldContainer[Region]
    def __init__(self, regions: _Optional[_Iterable[_Union[Region, _Mapping]]] = ...) -> None: ...
