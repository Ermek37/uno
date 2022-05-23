import json

with open("config.json","r") as f:
    config = json.loads(f.read())

TOKEN=config.get("token")
WORKERS=config.get("workers", 32)
ADMIN_LIST = config.get("admin_list", None)
OPEN_LOBBY = config.get("open_lobby", True)
ENABLE_TRANSLATIONS = config.get("enable_translations", False)
DEFAULT_GAMEMODE = config.get("default_gamemode", "fast")
WAITING_TIME = config.get("waiting_time", 120)
TIME_REMOVAL_AFTER_SKIP = config.get("time_removal_after_skip", 20)
MIN_FAST_TURN_TIME = config.get("min_fast_turn_time", 15)
MIN_PLAYERS = config.get("min_players", 2)