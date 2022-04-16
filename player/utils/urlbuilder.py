from urllib.parse import urljoin, urlencode

from player.config import PlayerConfig


def build_url(path, params):
    config = PlayerConfig.instance()
    host = config.get_referee_host()
    query = "?" + urlencode(params)
    return urljoin(host, path + query)


def get_notify_attack_url(game_id, guessed_number, opponent):
    path = "/notify-attack"
    params = {
        "guessed_number": guessed_number,
        "game-id": game_id,
        "opponent": opponent,
    }
    return build_url(path, params)


def get_notify_status(game_id, defended):
    path = "/notify-status"
    params = {
        "game-id": game_id,
        "defended": defended,
    }
    return build_url(path, params)


def get_join_championship_url(name):
    path = "/join-championship"
    params = {
        "name": name,
    }
    return build_url(path, params)
