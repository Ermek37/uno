import random
import logging
import card as c

from datetime import datetime
from telegram import Message, Chat
from config import TIME_REMOVAL_AFTER_SKIP, MIN_FAST_TURN_TIME
from errors import DeckEmptyError, NotEnoughPlayersError
from internationalization import __, _
from shared_vars import gm
from user_setting import UserSetting
from utils import send_async, display_name, game_is_running

logger = logging.getLogger(__name__)

class Countdown(object):
    player = None
    job_queue = None

    def __init__(self, player, job_queue):
        self.player = player
        self.job_queue = job_queue

def do_skip(bot, player, job_queue=None):
    game = player.game
    chat = game.chat
    skipped_player = game.current_player
    next_player = game.current_player.next

    if skipped_player.waiting_time > 0:
        skipped_player.anti_cheat += 1
        skipped_player.waiting_time -= TIME_REMOVAL_AFTER_SKIP
        if (skipped_player.waiting_time < 0):
            skipped_player.waiting_time = 0

        try:
            skipped_player.draw()
        except DeckEmptyError:
            pass

        n = skipped_player.waiting_time
        send_async(bot, chat.id,
                   text=("Waiting time to skip this player has "
                        "been reduced to {time} seconds.\n"
                        "Next player: {name}", multi=game.translate)
                   .format(time=n,
                           name=display_name(next_player.user))
        )
        logger.info("{player} was skipped! "
                    .format(player=display_name(player.user)))
        game.turn()
        if job_queue:
            start_player_countdown(bot, game, job_queue)

    else:
        try:
            gm.leave_game(skipped_player.user, chat)
            send_async(bot, chat.id,
                       text=("{name1} ran out of time "
                            "and has been removed from the game!\n"
                            "Next player: {name2}", multi=game.translate)
                       .format(name1=display_name(skipped_player.user),
                               name2=display_name(next_player.user)))
            logger.info("{player} was skipped! "
                    .format(player=display_name(player.user)))
            if job_queue:
                start_player_countdown(bot, game, job_queue)

        except NotEnoughPlayersError:
            send_async(bot, chat.id,
                       text=("{name} ran out of time "
                               "and has been removed from the game!\n"
                               "The game ended.", multi=game.translate)
                       .format(name=display_name(skipped_player.user)))

            gm.end_game(chat, skipped_player.user)



