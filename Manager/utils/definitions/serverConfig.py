import random
class Player:
    def __init__(self, name: str, steamID: str):
        self.name: str = name
        self.steamID: str = steamID + ""

    def to_dict(self):
        """Returns the player data as a dictionary."""
        return {str(self.steamID) + "": self.name}

class Team:
    def __init__(self, name: str, players: list[Player], tag: str = "Test"):
        self.name: str = name
        self.players: list[Player] = players
        self.tag: str = tag

    def to_dict(self):
        """Returns the team data in the expected format."""
        return {
            "id": str(random.randint(0, 1000)),
            "name": self.name,
            "tag": self.tag,
            "flag": "FR",
            "players": {str(player.steamID) + "": player.name for player in self.players}
        }

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
                 matchid: str,
                 title: str,
                 num_maps: int,
                 players_per_team: int,
                 min_players_to_ready: int,
                 skip_veto: bool,
                 maplist: list[str],
                 veto_first: str,
                 favored_percentage_team1: int,
                 team1: Team,
                 team2: Team,
                 spectators: Spectators,
                 cvars: list[CVar]):
        self.matchid: str = matchid
        self.title: str = title
        self.maplist: list[str] = maplist
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

    def to_dict(self):
        """Returns the game data in the expected JSON format."""
        return {
            "maplist": self.maplist,
            "team1": self.team1.to_dict(),
            "team2": self.team2.to_dict(),
            "matchid": self.matchid,
            "num_maps": self.num_maps,
            "players_per_team": self.players_per_team,
            "min_players_to_ready": self.min_players_to_ready,
            "max_rounds": 24,
            "max_overtime_rounds": 6,
            "vote_timeout": 60000,
            "g5_api_url":f'http://localhost:8081/events/{self.matchid}',
            "vote_map": "de_inferno",
            "server_locale": "fr",
            "g5_api_header" : "test",
            "g5_api_headervalue" : "test",
            "allow_suicide": False,
            "eventula_apistats_url": f'http://localhost:8081/eventula/{self.matchid}',
            'eventula_apistats_token': 'B test'
        }








