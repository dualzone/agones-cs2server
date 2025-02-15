from dataclasses import asdict, dataclass, field
from typing import List, Dict

@dataclass
class Player:
    name: str
    steamID: str

    def to_dict(self) -> Dict[str, str]:
        return {self.steamID: self.name}

@dataclass
class Team:
    name: str
    players: List[Player]

    def to_dict(self) -> Dict[str, any]:
        return {
            "name": self.name,
            "players": {player.steamID: player.name for player in self.players}
        }


@dataclass
class Spectators:
    players: List[Player]

    def to_dict(self) -> Dict[str, any]:
        return {
            "players": {player.steamID: player.name for player in self.players}
        }


@dataclass
class CVar:
    name: str
    value: str

@dataclass
class Game:
    matchid: int
    num_maps: int
    players_per_team: int
    maplist: List[str]
    team1: Team
    team2: Team
    spectators: Spectators
    cvars: List[CVar]
    clinch_series: bool = True
    skip_veto: bool = False
    veto_first: str = "random"
    side_type: str = "standard"

    def to_dict(self) -> Dict[str, any]:
        return {
            "matchid": self.matchid, #
            "team1": self.team1.to_dict(),
            "team2": self.team2.to_dict(),
            "num_maps": self.num_maps,#
            "maplist": self.maplist,
            "spectators": self.spectators.to_dict(),
            "clinch_series": self.clinch_series,
            "players_per_team": self.players_per_team,#
            "cvars": {cvar.name: cvar.value for cvar in self.cvars},
            "skip_veto": self.skip_veto,
            "veto_first": self.veto_first,
            "side_type": self.side_type
        }








