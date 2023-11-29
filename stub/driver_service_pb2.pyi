from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TaskType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    Map: _ClassVar[TaskType]
    Reduce: _ClassVar[TaskType]
    Idle: _ClassVar[TaskType]
    ShutDown: _ClassVar[TaskType]
Map: TaskType
Reduce: TaskType
Idle: TaskType
ShutDown: TaskType

class TaskInfo(_message.Message):
    __slots__ = ["type", "id", "M", "files"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    M_FIELD_NUMBER: _ClassVar[int]
    FILES_FIELD_NUMBER: _ClassVar[int]
    type: TaskType
    id: int
    M: int
    files: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, type: _Optional[_Union[TaskType, str]] = ..., id: _Optional[int] = ..., M: _Optional[int] = ..., files: _Optional[_Iterable[str]] = ...) -> None: ...
