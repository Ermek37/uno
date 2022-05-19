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

    def _first_card_(self):
        # In case that the player did not select a game mode
        if not self.deck.cards:
            self.set_mode(DEFAULT_GAMEMODE)

        # The first card should not be a special card
        while not self.last_card or self.last_card.special:
            self.last_card = self.deck.draw()
            # If the card drawn was special, return it to the deck and loop again
            if self.last_card.special:
                self.deck.dismiss(self.last_card)

        self.play_card(self.last_card)

    def play_card(self, card):
    
        self.deck.dismiss(self.last_card)
        self.last_card = card

        self.logger.info("Playing card " + repr(card))
        if card.value == c.SKIP:
            self.turn()
        elif card.special == c.DRAW_FOUR:
            self.draw_counter += 4
            self.logger.debug("Draw counter increased by 4")
        elif card.value == c.DRAW_TWO:
            self.draw_counter += 2
            self.logger.debug("Draw counter increased by 2")
        elif card.value == c.REVERSE:
            # Special rule for two players
            if self.current_player is self.current_player.next.next:
                self.turn()
            else:
                self.reverse()

        # Don't turn if the current player has to choose a color
        if card.special not in (c.CHOOSE, c.DRAW_FOUR):
            self.turn()
        else:
            self.logger.debug("Choosing Color...")
            self.choosing_color = True

    def choose_color(self, color):
        self.last_card.color = color
        self.turn()
