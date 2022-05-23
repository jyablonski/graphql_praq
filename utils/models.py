from sqlalchemy import Column, Integer, String, Float, ForeignKey, select
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.orm import Session

from .database import Base
from .discord_hook import discord_message

# my version - this is like the SQLAlchemy way of defining schema.
class Standings(Base):
    __tablename__ = "prod_standings"

    rank: str = Column(String, unique=True, nullable=False)
    team: str = Column(String, unique=True, primary_key=True, nullable=False)
    team_full: str = Column(String, unique=True, nullable=False)
    conference: str = Column(String, nullable=False)
    wins: int = Column(Integer, nullable=False)
    losses: int = Column(Integer, nullable=False)
    games_played: int = Column(Integer, nullable=False)
    win_pct: str = Column(Float, nullable=False)
    active_injuries: int = Column(Integer, nullable=False)
    active_protocols: int = Column(Integer, nullable=False)
    last_10: str = Column(String, nullable=False)


def get_standings(db: Session, limit: int = 250):
    query = select(Standings).limit(limit)

    result = db.execute(query).unique()
    discord_message(Standings.__tablename__)
    return result.scalars()


class Scorers(Base):
    __tablename__ = "prod_scorers"

    player: str = Column(String, unique=True, primary_key=True, nullable=False)
    team: str = Column(String, unique=True, nullable=False)
    full_team: str = Column(String, unique=True, nullable=False)
    season_avg_ppg: float = Column(Float)
    playoffs_avg_ppg: float = Column(Float, nullable=True)
    season_ts_percent: float = Column(Float)
    playoffs_ts_percent: float = Column(Float, nullable=True)
    games_played: int = Column(Integer)
    playoffs_games_played: int = Column(Integer, nullable=True)
    ppg_rank: int = Column(Integer)
    top20_scorers: str = Column(String)
    player_mvp_calc_adj: float = Column(Float)
    games_missed: int = Column(Integer)
    penalized_games_missed: int = Column(Integer)
    top5_candidates: str = Column(String)
    mvp_rank: str = Column(Integer)


def get_scorers(db: Session, limit: int = 250):
    query = select(Scorers).limit(limit)

    result = db.execute(query).unique()
    discord_message(Scorers.__tablename__)
    return result.scalars()
