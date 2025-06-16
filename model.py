from sqlalchemy import (
    Column, Integer, Float, String, ForeignKey, create_engine
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Player(Base):
    __tablename__ = "players"
    id       = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    level    = Column(Integer, default=1)
    exp      = Column(Integer, default=0)
    money    = Column(Float,   default=100.0)
    wins     = Column(Integer, default=0)

    monsters      = relationship("PlayerMonster", back_populates="player")
    achievements  = relationship("Achievement", secondary="player_achievements")

class MonsterSpecies(Base):
    __tablename__ = "monster_species"
    id, name, type = (Column(Integer, primary_key=True),
                      Column(String, unique=True, nullable=False),
                      Column(String, nullable=False))
    base_stats = Column(String)           # JSON str
    rarity     = Column(Float)
    abilities  = Column(String)           # JSON str list
    evolves_to = Column(String, nullable=True)  # simple evolution chain

class PlayerMonster(Base):
    __tablename__ = "player_monsters"
    id         = Column(Integer, primary_key=True)
    player_id  = Column(Integer, ForeignKey("players.id"))
    species_id = Column(Integer, ForeignKey("monster_species.id"))
    level      = Column(Integer, default=1)
    current_hp = Column(Integer)

    player  = relationship("Player", back_populates="monsters")
    species = relationship("MonsterSpecies")

class Battle(Base):
    __tablename__ = "battles"
    id         = Column(Integer, primary_key=True)
    player1_id = Column(Integer, ForeignKey("players.id"))
    player2_id = Column(Integer, ForeignKey("players.id"), nullable=True)
    winner_id  = Column(Integer, ForeignKey("players.id"), nullable=True)
    battle_log = Column(String)

class Trade(Base):
    __tablename__ = "trades"
    id               = Column(Integer, primary_key=True)
    from_player_id   = Column(Integer, ForeignKey("players.id"))
    to_player_id     = Column(Integer, ForeignKey("players.id"))
    offered_monsters   = Column(String)
    requested_monsters = Column(String)
    status           = Column(String, default="Pending")

class Achievement(Base):
    __tablename__ = "achievements"
    id          = Column(Integer, primary_key=True)
    name        = Column(String, unique=True)
    description = Column(String)

class PlayerAchievement(Base):
    __tablename__ = "player_achievements"
    id             = Column(Integer, primary_key=True)
    player_id      = Column(Integer, ForeignKey("players.id"))
    achievement_id = Column(Integer, ForeignKey("achievements.id"))

# ─ engine & session ─
engine  = create_engine("sqlite:///Monster_inc.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
