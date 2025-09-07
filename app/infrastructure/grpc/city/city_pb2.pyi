from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class City(_message.Message):
    __slots__ = ("id", "district_id", "name", "obj_type", "population")
    ID_FIELD_NUMBER: _ClassVar[int]
    DISTRICT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OBJ_TYPE_FIELD_NUMBER: _ClassVar[int]
    POPULATION_FIELD_NUMBER: _ClassVar[int]
    id: str
    district_id: str
    name: str
    obj_type: str
    population: int
    def __init__(self, id: _Optional[str] = ..., district_id: _Optional[str] = ..., name: _Optional[str] = ..., obj_type: _Optional[str] = ..., population: _Optional[int] = ...) -> None: ...

class NewCityDTO(_message.Message):
    __slots__ = ("district_id", "name", "obj_type", "population")
    DISTRICT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OBJ_TYPE_FIELD_NUMBER: _ClassVar[int]
    POPULATION_FIELD_NUMBER: _ClassVar[int]
    district_id: str
    name: str
    obj_type: str
    population: int
    def __init__(self, district_id: _Optional[str] = ..., name: _Optional[str] = ..., obj_type: _Optional[str] = ..., population: _Optional[int] = ...) -> None: ...

class CityIdRequest(_message.Message):
    __slots__ = ("city_id",)
    CITY_ID_FIELD_NUMBER: _ClassVar[int]
    city_id: str
    def __init__(self, city_id: _Optional[str] = ...) -> None: ...

class DistrictIdRequest(_message.Message):
    __slots__ = ("district_id",)
    DISTRICT_ID_FIELD_NUMBER: _ClassVar[int]
    district_id: str
    def __init__(self, district_id: _Optional[str] = ...) -> None: ...

class CityList(_message.Message):
    __slots__ = ("cities",)
    CITIES_FIELD_NUMBER: _ClassVar[int]
    cities: _containers.RepeatedCompositeFieldContainer[City]
    def __init__(self, cities: _Optional[_Iterable[_Union[City, _Mapping]]] = ...) -> None: ...

class CityIdResponse(_message.Message):
    __slots__ = ("city_id",)
    CITY_ID_FIELD_NUMBER: _ClassVar[int]
    city_id: str
    def __init__(self, city_id: _Optional[str] = ...) -> None: ...
