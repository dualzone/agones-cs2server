from typing import List, Optional
from pydantic import BaseModel

class Team(BaseModel):
    id: str
    name: str


class PlayerStats(BaseModel):
    kills: int
    deaths: int
    assists: int
    flash_assists: int
    team_kills: int
    suicides: int
    damage: int
    utility_damage: int
    enemies_flashed: int
    friendlies_flashed: int
    knife_kills: int
    headshot_kills: int
    rounds_played: int
    bomb_defuses: int
    bomb_plants: int
    one_k: int = 0
    two_k: int = 0
    three_k: int = 0
    four_k: int = 0
    five_k: int = 0
    one_v1: int = 0
    one_v2: int = 0
    one_v3: int = 0
    one_v4: int = 0
    one_v5: int = 0
    first_kills_t: int = 0
    first_kills_ct: int = 0
    first_deaths_t: int = 0
    first_deaths_ct: int = 0
    trade_kills: int = 0
    kast: int
    score: int
    mvp: int


class Player(BaseModel):
    steamid: str
    name: str
    stats: PlayerStats


class TeamDetails(BaseModel):
    id: str
    name: str
    series_score: Optional[int] = 0
    score: Optional[int] = 0
    score_ct: Optional[int] = 0
    score_t: Optional[int] = 0
    side: Optional[str] = "ct"
    starting_side: Optional[str] = "ct"
    players: List[Player] = []


class EventBase(BaseModel):
    event: str
    matchid: int


class SeriesStartEvent(EventBase):
    team1: Team
    team2: Team


class MapResultEvent(EventBase):
    map_number: int
    team1: TeamDetails
    team2: TeamDetails
    winner: dict


class SeriesEndEvent(EventBase):
    team1_series_score: int
    team2_series_score: int
    winner: dict
    time_until_restore: Optional[int] = None


class SidePickedEvent(EventBase):
    team: str
    map_name: str
    side: str
    map_number: int


class MapPickedEvent(EventBase):
    team: str
    map_name: str
    map_number: int


class MapVetoedEvent(EventBase):
    team: str
    map_name: str

class MatchGoingLiveEvent(EventBase):
    map_number: int

class RoundEndEvent(EventBase):
    map_number: int
    round_number: int
    round_time: int
    reason: int
    winner: dict
    team1: TeamDetails
    team2: TeamDetails