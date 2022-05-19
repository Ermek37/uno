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
            for g in list(self.chatid_games[chat_id]):
                    if not g.players:
                            self.chatid_games[chat_id].remove(g)

        self.chatid_games[chat_id].append(game)
        return game
        
        def leave_game(self, user, chat):
            player = self.player_for_user_in_chat(user, chat)
            players = self.userid_players.get(user.id, list())

        if not player:
            games = self.chatid_games[chat.id]
            for g in games:
                for p in g.players:
                    if p.user.id == user.id:
                        if p is g.current_player:
                            g.turn()

                        p.leave()
                        return

            raise NoGameInChatError

        game = player.game

        if len(game.players) < 3:
            raise NotEnoughPlayersError()

        if player is game.current_player:
            game.turn()

        player.leave()
        players.remove(player)

        if self.userid_current.get(user.id, None) is player:
            if players:
                self.userid_current[user.id] = players[0]
            else:
                del self.userid_current[user.id]
                del self.userid_players[user.id]
