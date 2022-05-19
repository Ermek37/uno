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
    
    def players(self):
        players = list()
        if not self.current_player:
            return players

        current_player = self.current_player
        itplayer = current_player.next
        players.append(current_player)
        while itplayer and itplayer is not current_player:
            players.append(itplayer)
            itplayer = itplayer.next
        return players

    def start(self):
        if self.mode == None or self.mode != "wild":
            self.deck._fill_classic_()
        else:
            self.deck._fill_wild_()

        self._first_card_()
        self.started = True

    def set_mode(self, mode):
        self.mode = mode

    def reverse(self):
        self.reversed = not self.reversed

    def turn(self):
        self.logger.debug("Next Player")
        self.current_player = self.current_player.next
        self.current_player.drew = False
        self.current_player.turn_started = datetime.now()
        self.choosing_color = False
