from datetime import datetime
import typing
import strawberry
from strawberry.extensions import Extension
from strawberry.asgi import GraphQL
from fastapi import FastAPI

from utils.database import SessionLocal
from utils.definitions import (
    Team,
    Player,
    Team_Original,
    get_players,
    get_teams_original,
)
from utils.models import get_teams


class SQLAlchemySession(Extension):
    def on_request_start(self):
        self.execution_context.context["db"] = SessionLocal()

    def on_request_end(self):
        self.execution_context.context["db"].close()


# never actually used this, i dont think you ever want to be adding bs this way?
@strawberry.type
class Mutation:
    @strawberry.field
    def add_player(self, player: str, team: str, ppg: float) -> Player:
        ...


@strawberry.type
class Query:
    # THESE 3 lines are defining the schema in the documentation on the graphql site
    # you can OPTIONALLY also provide the actual query mechanism, like i did for players and teams
    # all_teams i did it separately
    players: typing.List[Player] = strawberry.field(resolver=get_players)
    teams: typing.List[Team_Original] = strawberry.field(resolver=get_teams_original)
    all_teams: typing.List[Team]

    @strawberry.field
    def all_teams(self, info, limit: int = 250) -> typing.List[Team]:
        db = info.context["db"]
        teams = get_teams(db, limit=limit) # i wrote this in the models.py script
        return teams


schema = strawberry.Schema(query=Query, extensions=[SQLAlchemySession])
