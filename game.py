import logging
from config import ADMIN_LIST, OPEN_LOBBY, DEFAULT_GAMEMODE
from datetime import datetime

from deck import Deck
import card as c

class Game(object):
    current_player = None
    reversed = False
    choosing_color = False
    started = False
    draw_counter = 0
    players_won = 0
    starter = None
    mode = DEFAULT_GAMEMODE
    job = None
    owner = ADMIN_LIST
    open = OPEN_LOBBY
    