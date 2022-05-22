from telegram import ParseMode
from telegram.ext import CommandHandler

from user_setting import UserSetting
from utils import send_async
from shared_vars import dispatcher
from internationalization import _, user_locale

@user_locale
def help_handler(bot, update):
    """Handler for the /help command"""
    help_text = _("Follow these steps:\n\n"
      "1. Add this bot to a group\n"
      "2. In the group, start a new game with /new or join an already"
      " running game with /join\n"
      "3. After at least two players have joined, start the game with"
      " /start\n"
      "4. Type <code>@unobot</code> into your chat box and hit "
      "<b>space</b>, or click the <code>via @unobot</code> text "
      "next to messages. You will see your cards (some greyed out), "
      "any extra options like drawing, and a <b>?</b> to see the "
      "current game state. The <b>greyed out cards</b> are those you "
      "<b>can not play</b> at the moment. Tap an option to execute "
      "the selected action.\n"
      "Players can join the game at any time. To leave a game, "
      "use /leave. If a player takes more than 90 seconds to play, "
      "you can use /skip to skip that player. Use /notify_me to "
      "receive a private message when a new game is started.\n\n"
      "<b>Language</b> and other settings: /settings\n"
      "Other commands (only game creator):\n"
      "/close - Close lobby\n"
      "/open - Open lobby\n"
      "/kill - Terminate the game\n"
      "/kick - Select a player to kick "
      "by replying to him or her\n"
      "/enable_translations - Translate relevant texts into all "
      "languages spoken in a game\n"
      "/disable_translations - Use English for those texts\n\n"
      "<b>Experimental:</b> Play in multiple groups at the same time. "
      "Press the <code>Current game: ...</code> button and select the "
      "group you want to play a card in.\n"
      "If you enjoy this bot, "
      "<a href=\"https://telegram.me/storebot?start=mau_mau_bot\">"
      "rate me</a>, join the "
      "<a href=\"https://telegram.me/unobotupdates\">update channel</a>"
      " and buy an UNO card game.")

    send_async(bot, update.message.chat_id, text=help_text,
               parse_mode=ParseMode.HTML, disable_web_page_preview=True)