class Player:
    def __init__(self, name: str, steamID: str):
        self.name: str = name
        self.steamID: str = steamID

class Team:
    def __init__(self, name: str, players: list[Player]):
        self.name: str = name
        self.players: list[Player] = players

class CVar:
    def __init__(self, name: str, value: str):
        self.name: str = name
        self.value: str = value

class Spectators:
    def __init__(self, players: list[Player]):
        self.name: str = "Spectators"
        self.players: list[Player] = players

class Game:
    def __init__(self,
                 id: str,
                 title: str,
                 num_maps: int,
                 players_per_team: int,
                 min_players_to_ready: int,
                 skip_veto: bool,
                 veto_first: str,
                 favored_percentage_team1: int,
                 team1: Team,
                 team2: Team,
                 spectators: Spectators,
                 cvars: list[CVar]):
        self.id: str = id
        self.title: str = title
        self.num_maps: int = num_maps
        self.players_per_team: int = players_per_team
        self.min_players_to_ready: int = min_players_to_ready
        self.skip_veto: bool = skip_veto
        self.veto_first: str = veto_first
        self.favored_percentage_team1: int = favored_percentage_team1
        self.team1: Team = team1
        self.team2: Team = team2
        self.spectators: Spectators = spectators
        self.cvars: list[CVar] = cvars
        self.min_spectators_to_ready: int = 0
        self.coaches_per_team: int = 0








