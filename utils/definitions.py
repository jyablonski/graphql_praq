from datetime import date
from typing import Optional

import strawberry

# the graphql way of defining schema.
@strawberry.type
class Standings:
    rank: str
    team: str
    team_full: str
    conference: str
    wins: int
    losses: int
    games_played: int
    win_pct: str
    active_injuries: int
    active_protocols: int
    last_10: str


@strawberry.type
class Scorers:
    player: str
    team: str
    full_team: str
    season_avg_ppg: float
    playoffs_avg_ppg: Optional[float]
    season_ts_percent: Optional[float]
    playoffs_ts_percent: Optional[float]
    games_played: int
    playoffs_games_played: Optional[int]
    ppg_rank: int
    top20_scorers: str
    player_mvp_calc_adj: float
    games_missed: int
    penalized_games_missed: int
    top5_candidates: str
    mvp_rank: str


@strawberry.type
class Team_Ratings:
    team: str
    team_acronym: str
    w: int
    l: int
    ortg: float
    drtg: float
    nrtg: float
    team_logo: str
    nrtg_rank: str
    drtg_rank: str
    ortg_rank: str


@strawberry.type
class Twitter_Comments:
    scrape_date: date
    username: str
    tweet: str
    url: str
    likes_count: int
    retweets_count: int
    replies_count: int
    compound: float
    neg: float
    neu: float
    pos: float


@strawberry.type
class Reddit_Comments:
    scrape_date: date
    author: str
    comment: str
    flair: Optional[str]
    score: int
    url: str
    compound: float
    neg: float
    neu: float
    pos: float


@strawberry.type
class Injuries:
    player: str
    team_acronym: str
    team: str
    date: str
    status: str
    injury: str
    description: str
    total_injuries: int
    team_active_injuries: int
    team_active_protocols: int


@strawberry.type
class Game_Types:
    game_type: str
    type: str
    n: int
    explanation: str


@strawberry.type
class Player:
    name: str
    team: str
    ppg: float


@strawberry.type
class Team_Original:
    name: str
    color: str
    players: str


# these are dummy "fixtures" with the schema provided from above so we can query them in graphql
# normally you'd query this data from SQL
def get_players():
    return [
        Player(
            name="Stephen Curry",
            team="Golden State Warriors",
            ppg=25.5,
        ),
    ]


def get_teams_original():
    return [
        Team_Original(
            name="Golden State Warriors",
            color="Yellow",
            players="Stephen Curry xd this dont work",
        ),
    ]
