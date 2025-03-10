import json
from utils.redis.redisClient import RedisClient
from utils.definitions.serverConfig import Game, Team, Player, CVar, Spectators


class ScanConfig:
    def __init__(self, uuid: str):
        self.uuid = uuid
        self.redis_client: RedisClient = RedisClient().get_client()

    def get_game_instance(self) -> Game:
        game_config_key = f"gameserver:{self.uuid}:config"
        game_vars_key = f"gameserver:{self.uuid}:vars"
        team1_key = f"gameserver:{self.uuid}:team1:config"
        team2_key = f"gameserver:{self.uuid}:team2:config"
        team1_players_key = f"gameserver:{self.uuid}:team1:players"
        team2_players_key = f"gameserver:{self.uuid}:team2:players"
        spectators_key = f"gameserver:{self.uuid}:spectators"
        maps_key = f"gameserver:{self.uuid}:maps"

        # Récupération des données de configuration du jeu
        game_config = self.redis_client.hgetall(game_config_key)
        game_vars = self.redis_client.hgetall(game_vars_key)
        game_maps = self.redis_client.lrange(maps_key, 0, -1)

        # Vérification de la présence des clés requises
        required_keys = [b'id', b'title', b'num_maps', b'players_per_team', b'min_players_to_ready',
                         b'clinch_series', b'skip_veto', b'veto_first', b'side_type']
        for key in required_keys:
            if key not in game_config:
                raise ValueError(f"Missing required key in game config: {key.decode()}")

        players_per_team = int(game_config[b'players_per_team'])

        # Vérification que la liste des maps n'est pas vide
        if not game_maps:
            raise ValueError("The map list cannot be empty.")

        # Récupération des joueurs des équipes
        team1_config = self.redis_client.hgetall(team1_key)
        team2_config = self.redis_client.hgetall(team2_key)

        team1_name = team1_config.get(b'name')
        team2_name = team2_config.get(b'name')

        team1_players_data = self.redis_client.hgetall(team1_players_key)
        team2_players_data = self.redis_client.hgetall(team2_players_key)
        spectators_data = self.redis_client.hgetall(spectators_key)

        # Vérification que chaque équipe a bien un nom
        if not team1_name or not team2_name:
            raise ValueError("Both teams must have a name.")

        # Création des instances de Player
        team1_players = [Player(name=name.decode(), steamID=steamid.decode()) for steamid, name in
                         team1_players_data.items()]
        team2_players = [Player(name=name.decode(), steamID=steamid.decode()) for steamid, name in
                         team2_players_data.items()]
        spectators_players = [Player(name=name.decode(), steamID=steamid.decode()) for steamid, name in
                              spectators_data.items()]

        # Vérification que chaque équipe a le bon nombre de joueurs
        if len(team1_players) != players_per_team:
            raise ValueError(f"Team 1 must have exactly {players_per_team} players, found {len(team1_players)}.")
        if len(team2_players) != players_per_team:
            raise ValueError(f"Team 2 must have exactly {players_per_team} players, found {len(team2_players)}.")

        # Création des équipes
        team1 = Team(name=team1_name.decode(), players=team1_players)
        team2 = Team(name=team2_name.decode(), players=team2_players)
        spectators = Spectators(players=spectators_players)

        # Création des cvars
        cvars = [CVar(name=k.decode(), value=v.decode()) for k, v in game_vars.items()]
        cvars.append(CVar(name="matchzy_minimum_ready_required", value=game_config[b'min_players_to_ready'].decode()))
        cvars.append(CVar(name="hostname", value=team1.name + " vs " + team2.name + " - Match ID: " + game_config[b'id'].decode()))
        cvars.append(CVar(name="matchzy_show_credits_on_match_start", value=0))
        cvars.append(CVar(name="matchzy_remote_log_url", value=f'http://localhost:8081/events/{self.uuid}'))

        # Création et retour de l'instance Game
        return Game(
            matchid=game_config[b'id'].decode(),
            num_maps=int(game_config[b'num_maps']),
            maplist=[map.decode() for map in game_maps],
            players_per_team=players_per_team,
            team1=team1,
            team2=team2,
            spectators=spectators,
            cvars=cvars,
            side_type=game_config[b'side_type'].decode(),
            clinch_series=self.__parse_bool(game_config[b'clinch_series'].decode()),
            skip_veto=self.__parse_bool(game_config[b'skip_veto'].decode()),
            veto_first=game_config[b'veto_first'].decode()
        )

    def __parse_bool(self, string: str) -> bool:
        string = string.lower()
        if string in ('y', 'yes', 't', 'true', 'on', '1'):
            return True
        else:
            return False

    def to_json(self) -> str:
        game = self.get_game_instance()
        return json.dumps(game, default=lambda o: o.__dict__, indent=4)