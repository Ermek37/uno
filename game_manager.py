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

        # If this is the selected game, switch to another
        if self.userid_current.get(user.id, None) is player:
            if players:
                self.userid_current[user.id] = players[0]
            else:
                del self.userid_current[user.id]
                del self.userid_players[user.id]


def join_game(self, user, chat):
        """ Create a player from the Telegram user and add it to the game """
        self.logger.info("Joining game with id " + str(chat.id))

        try:
            game = self.chatid_games[chat.id][-1]
        except (KeyError, IndexError):
            raise NoGameInChatError()

        if not game.open:
            raise LobbyClosedError()

        if user.id not in self.userid_players:
            self.userid_players[user.id] = list()

        players = self.userid_players[user.id]

        # Don not re-add a player and remove the player from previous games in
        # this chat, if he is in one of them
        for player in players:
            if player in game.players:
                raise AlreadyJoinedError()

        try:
            self.leave_game(user, chat)
        except NoGameInChatError:
            pass
        except NotEnoughPlayersError:
            self.end_game(chat, user)

            if user.id not in self.userid_players:
                self.userid_players[user.id] = list()

            players = self.userid_players[user.id]

        player = Player(game, user)
        if game.started:
            player.draw_first_hand()

        players.append(player)
        self.userid_current[user.id] = player


