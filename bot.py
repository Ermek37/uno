import logging
from datetime import datetime

from telegram import ParseMode, InlineKeyboardMarkup, \
    InlineKeyboardButton
from telegram.ext import InlineQueryHandler, ChosenInlineResultHandler, \
    CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram.ext.dispatcher import run_async

import card as c
import settings
import simple_commands
from actions import do_skip, do_play_card, do_draw, do_call_bluff, start_player_countdown
from config import WAITING_TIME, DEFAULT_GAMEMODE, MIN_PLAYERS
from errors import (NoGameInChatError, LobbyClosedError, AlreadyJoinedError,
                    NotEnoughPlayersError, DeckEmptyError)
from internationalization import _, __, user_locale, game_locales
from results import (add_call_bluff, add_choose_color, add_draw, add_gameinfo,
                     add_no_game, add_not_started, add_other_cards, add_pass,
                     add_card, add_mode_classic, add_mode_fast, add_mode_wild, add_mode_text)
from shared_vars import gm, updater, dispatcher
from simple_commands import help_handler
from start_bot import start_bot
from utils import display_name
from utils import send_async, answer_async, error, TIMEOUT, user_is_creator_or_admin, user_is_creator, game_is_running

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

@user_locale
def notify_me(bot, update):
    """Handler for /notify_me command, pm people for next game"""
    chat_id = update.message.chat_id
    if update.message.chat.type == 'private':
        send_async(bot,
                   chat_id,
                   text=_("Send this command in a group to be notified "
                          "when a new game is started there."))
    else:
        try:
            gm.remind_dict[chat_id].add(update.message.from_user.id)
        except KeyError:
            gm.remind_dict[chat_id] = {update.message.from_user.id}




