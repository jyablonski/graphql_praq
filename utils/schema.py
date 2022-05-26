from datetime import datetime
from typing import List
import strawberry
from strawberry.extensions import Extension
from strawberry.asgi import GraphQL
from fastapi import FastAPI

from utils.database import SessionLocal
from utils.definitions import (
    Injuries,
    Game_Types,
    Standings,
    Scorers,
    Player,
    Reddit_Comments,
    Team_Original,
    Team_Ratings,
    Twitter_Comments,
    get_players,
    get_teams_original,
)
from utils.models import get_standings, get_scorers, get_team_ratings, get_twitter_comments, get_reddit_comments, get_injuries, get_game_types


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
    players: List[Player] = strawberry.field(resolver=get_players)
    teams: List[Team_Original] = strawberry.field(resolver=get_teams_original)

    all_teams: List[Standings]
    scorer_stats: List[Scorers]
    team_ratings: List[Team_Ratings]
    twitter_comments: List[Twitter_Comments]
    reddit_comments: List[Reddit_Comments]
    injuries: List[Injuries]
    game_types: List[Game_Types]

    @strawberry.field
    def all_teams(self, info, limit: int = 250) -> List[Standings]:
        db = info.context["db"]
        teams = get_standings(db, limit=limit)  # i wrote this in the models.py script
        return teams

    @strawberry.field
    def specific_teams(self, info, team_str: str, limit: int = 250) -> List[Standings]:
        db = info.context["db"]
        teams = get_standings(db, limit=limit)  # i wrote this in the models.py script
        return filter(lambda x: x.team == team_str, teams)

    @strawberry.field
    def scorer_stats(self, info, limit: int = 250) -> List[Scorers]:
        db = info.context["db"]
        scorers = get_scorers(db, limit=limit)  # i wrote this in the models.py script
        return scorers

    @strawberry.field
    def team_ratings(self, info, limit: int = 30) -> List[Team_Ratings]:
        db = info.context["db"]
        team_ratings_data = get_team_ratings(db, limit=limit)  # i wrote this in the models.py script
        return team_ratings_data

    @strawberry.field
    def twitter_comments(self, info, limit: int = 250) -> List[Twitter_Comments]:
        db = info.context["db"]
        twitter_comments_data = get_twitter_comments(db, limit=limit)  # i wrote this in the models.py script
        return twitter_comments_data

    @strawberry.field
    def reddit_comments(self, info, limit: int = 250) -> List[Reddit_Comments]:
        db = info.context["db"]
        reddit_comments_data = get_reddit_comments(db, limit=limit)  # i wrote this in the models.py script
        return reddit_comments_data

    @strawberry.field
    def injuries(self, info, limit: int = 100) -> List[Injuries]:
        db = info.context["db"]
        injuries_data = get_injuries(db, limit=limit)  # i wrote this in the models.py script
        return injuries_data

    @strawberry.field
    def game_types(self, info, limit: int = 6) -> List[Game_Types]:
        db = info.context["db"]
        game_types_data = get_game_types(db, limit=limit)  # i wrote this in the models.py script
        return game_types_data

schema = strawberry.Schema(query=Query, extensions=[SQLAlchemySession])
