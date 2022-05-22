import strawberry

from utils.models import Team as TeamModel # this is the only model i've actually created

# the graphql way of defining schema.
@strawberry.type
class Team:
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
