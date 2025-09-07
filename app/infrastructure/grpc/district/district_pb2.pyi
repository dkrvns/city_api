from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class District(_message.Message):
    __slots__ = ("id", "region_id", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    REGION_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    region_id: str
    name: str
    def __init__(self, id: _Optional[str] = ..., region_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class NewDistrictDTO(_message.Message):
    __slots__ = ("region_id", "name")
    REGION_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    region_id: str
    name: str
    def __init__(self, region_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class DistrictIdRequest(_message.Message):
    __slots__ = ("district_id",)
    DISTRICT_ID_FIELD_NUMBER: _ClassVar[int]
    district_id: str
    def __init__(self, district_id: _Optional[str] = ...) -> None: ...

class RegionIdRequest(_message.Message):
    __slots__ = ("region_id",)
    REGION_ID_FIELD_NUMBER: _ClassVar[int]
    region_id: str
    def __init__(self, region_id: _Optional[str] = ...) -> None: ...

class DistrictList(_message.Message):
    __slots__ = ("districts",)
    DISTRICTS_FIELD_NUMBER: _ClassVar[int]
    districts: _containers.RepeatedCompositeFieldContainer[District]
    def __init__(self, districts: _Optional[_Iterable[_Union[District, _Mapping]]] = ...) -> None: ...

class DistrictIdResponse(_message.Message):
    __slots__ = ("district_id",)
    DISTRICT_ID_FIELD_NUMBER: _ClassVar[int]
    district_id: str
    def __init__(self, district_id: _Optional[str] = ...) -> None: ...
