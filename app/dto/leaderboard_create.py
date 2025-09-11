from pydantic import BaseModel
from enum import Enum


class LeaderboardType(str, Enum):
    TABLE = "table"
    GRAPH = "graph"


class GenerateLeaderboardInput(BaseModel):
    type: LeaderboardType