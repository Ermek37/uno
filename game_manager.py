import logging

from game import Game
from player import Player
from errors import (AlreadyJoinedError, LobbyClosedError, NoGameInChatError,
                    NotEnoughPlayersError)


class GameManager(object):

    def __init__(self):
        self.chatid_games = dict()
        self.userid_players = dict()
        self.userid_current = dict()
        self.remind_dict = dict()

        self.logger = logging.getLogger(__name__)

    def new_game(self, chat):
        
        chat_id = chat.id

        self.logger.debug("Creating new game in chat " + str(chat_id))
        game = Game(chat)

        if chat_id not in self.chatid_games:
            self.chatid_games[chat_id] = list()

        # remove old games
        for g in list(self.chatid_games[chat_id]):
            if not g.players:
                self.chatid_games[chat_id].remove(g)

        self.chatid_games[chat_id].append(game)
        return game