import asyncio
import typing
from enum import Enum
from typing import Optional

from graphql import GraphQLError

import strawberry
from strawberry.file_uploads import Upload
from strawberry.permission import BasePermission
from strawberry.subscriptions.protocols.graphql_transport_ws.types import PingMessage
from strawberry.types import Info


class AlwaysFailPermission(BasePermission):
    message = "You are not authorized"

    def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        return False


@strawberry.enum
class Flavor(Enum):
    VANILLA = "vanilla"
    STRAWBERRY = "strawberry"
    CHOCOLATE = "chocolate"


@strawberry.input
class FolderInput:
    files: typing.List[Upload]


@strawberry.type
class DebugInfo:
    num_active_result_handlers: int
    is_connection_init_timeout_task_done: typing.Optional[bool]


@strawberry.type
class Query:
    @strawberry.field
    def hello(self, name: typing.Optional[str] = None) -> str:
        return f"Hello {name or 'world'}"

    @strawberry.field
    async def async_hello(self, name: str, delay: float = 0) -> str:
        await asyncio.sleep(delay)
        return f"Hello {name or 'world'}"

    @strawberry.field(permission_classes=[AlwaysFailPermission])
    def always_fail(self) -> Optional[str]:
        return "Hey"

    @strawberry.field
    def root_name(root) -> str:
        return type(root).__name__

    @strawberry.field
    async def exception(self, message: str) -> str:
        raise ValueError(message)
        return message


schema = strawberry.Schema(Query)
