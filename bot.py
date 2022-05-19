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


@user_locale
def new_game(bot, update):
    """Handler for the /new command"""
    chat_id = update.message.chat_id

    if update.message.chat.type == 'private':
        help_handler(bot, update)

    else:

        if update.message.chat_id in gm.remind_dict:
            for user in gm.remind_dict[update.message.chat_id]:
                send_async(bot,
                           user,
                           text=_("A new game has been started in {title}").format(
                                title=update.message.chat.title))

            del gm.remind_dict[update.message.chat_id]

        game = gm.new_game(update.message.chat)
        game.starter = update.message.from_user
        game.owner.append(update.message.from_user.id)
        game.mode = DEFAULT_GAMEMODE
        send_async(bot, chat_id,
                   text=_("Created a new game! Join the game with /join "
                          "and start the game with /start"))
                          
                          

@user_locale
def kill_game(bot, update):
    """Handler for the /kill command"""
    chat = update.message.chat
    user = update.message.from_user
    games = gm.chatid_games.get(chat.id)

    if update.message.chat.type == 'private':
        help_handler(bot, update)
        return

    if not games:
            send_async(bot, chat.id,
                       text=_("There is no running game in this chat."))
            return

    game = games[-1]

    if user_is_creator_or_admin(user, game, bot, chat):

        try:
            gm.end_game(chat, user)
            send_async(bot, chat.id, text=__("Game ended!", multi=game.translate))

        except NoGameInChatError:
            send_async(bot, chat.id,
                       text=_("The game is not started yet. "
                              "Join the game with /join and start the game with /start"),
                       reply_to_message_id=update.message.message_id)

    else:
        send_async(bot, chat.id,
                  text=_("Only the game creator ({name}) and admin can do that.")
                  .format(name=game.starter.first_name),
                  reply_to_message_id=update.message.message_id)




