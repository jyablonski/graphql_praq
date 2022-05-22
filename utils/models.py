from sqlalchemy import Column, Integer, String, Float, ForeignKey, select
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.orm import Session

from .database import Base

# my version - this is like the SQLAlchemy way of defining schema.
class Team(Base):
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


def get_teams(db: Session, limit: int = 250):
    query = select(Team).limit(limit)

    result = db.execute(query).unique()
    return result.scalars()
