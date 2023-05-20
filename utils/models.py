from datetime import date, datetime

from psycopg2 import Date
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    select,
    Date,
    PrimaryKeyConstraint,
    TIMESTAMP,
)
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.orm import Session

from .database import Base

# from .hooks import discord_message, sns_message

# my version - this is like the SQLAlchemy way of defining schema.
class Standings(Base):
    __tablename__ = "standings"

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
    # discord_message(Standings.__tablename__)
    # sns_message(Standings.__tablename__)
    return result.scalars()


class Scorers(Base):
    __tablename__ = "scorers"

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
    return result.scalars()


class Team_Ratings(Base):
    __tablename__ = "team_ratings"

    team: str = Column(String, unique=True, primary_key=True, nullable=False)
    team_acronym: str = Column(String, unique=True, nullable=False)
    w: int = Column(Integer, nullable=False)
    l: int = Column(Integer, nullable=False)
    ortg: float = Column(Float, nullable=False)
    drtg: float = Column(Float, nullable=False)
    nrtg: float = Column(Float, nullable=False)
    team_logo: str = Column(String, nullable=False)
    nrtg_rank: str = Column(String, nullable=False)
    drtg_rank: str = Column(String, nullable=False)
    ortg_rank: str = Column(String, nullable=False)


def get_team_ratings(db: Session, limit: int = 30):
    query = select(Team_Ratings).limit(limit)

    result = db.execute(query).unique()
    return result.scalars()


class Twitter_Comments(Base):
    __tablename__ = "twitter_comments"
    __table_args__ = (PrimaryKeyConstraint("scrape_ts", "username", "tweet"),)

    scrape_ts: datetime = Column(TIMESTAMP, nullable=False)
    username: str = Column(String, nullable=False)
    tweet: str = Column(String, nullable=False)
    url: str = Column(String, nullable=False)
    likes: int = Column(Integer, nullable=False)
    retweets: int = Column(Integer, nullable=False)
    compound: float = Column(Float, nullable=False)
    neg: float = Column(Float, nullable=False)
    neu: float = Column(Float, nullable=False)
    pos: float = Column(Float, nullable=False)


def get_twitter_comments(db: Session, limit: int = 250):
    query = select(Twitter_Comments).limit(limit)

    result = db.execute(query).unique()
    return result.scalars()


class Reddit_Comments(Base):
    __tablename__ = "reddit_comments"
    __table_args__ = (PrimaryKeyConstraint("scrape_date", "author", "comment"),)

    scrape_date: date = Column(Date, nullable=False)
    author: str = Column(String, nullable=False)
    comment: str = Column(String, nullable=False)
    flair: str = Column(String, nullable=True)
    score: int = Column(Integer, nullable=False)
    url: str = Column(String, nullable=False)
    compound: float = Column(Float, nullable=False)
    neg: float = Column(Float, nullable=False)
    neu: float = Column(Float, nullable=False)
    pos: float = Column(Float, nullable=False)


def get_reddit_comments(db: Session, limit: int = 250):
    query = select(Reddit_Comments).limit(limit)

    result = db.execute(query).unique()
    return result.scalars()


class Injuries(Base):
    __tablename__ = "injuries"
    __table_args__ = (PrimaryKeyConstraint("player", "injury", "description"),)

    player: str = Column(String, nullable=False)
    team_acronym: str = Column(String, nullable=False)
    team: str = Column(String, nullable=False)
    date: str = Column(String, nullable=False)
    status: str = Column(String, nullable=False)
    injury: str = Column(String, nullable=False)
    description: str = Column(String, nullable=False)
    total_injuries: int = Column(Integer, nullable=False)
    team_active_injuries: int = Column(Integer, nullable=False)
    team_active_protocols: int = Column(Integer, nullable=False)


def get_injuries(db: Session, limit: int = 100):
    query = select(Injuries).limit(limit)

    result = db.execute(query).unique()
    return result.scalars()


class Game_Types(Base):
    __tablename__ = "game_types"
    __table_args__ = (PrimaryKeyConstraint("game_type", "type"),)

    game_type: str = Column(String, nullable=False)
    type: str = Column(String, nullable=False)
    n: int = Column(Integer, nullable=False)
    explanation: str = Column(String, nullable=False)


def get_game_types(db: Session, limit: int = 8):
    query = select(Game_Types).limit(limit)

    result = db.execute(query).unique()
    return result.scalars()
