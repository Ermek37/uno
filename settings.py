from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, RegexHandler

from utils import send_async
from user_setting import UserSetting
from shared_vars import dispatcher
from locales import available_locales
from internationalization import _, user_locale


@user_locale
def show_settings(bot, update):
    chat = update.message.chat

    if update.message.chat.type != 'private':
        send_async(bot, chat.id,
                   text=_("Please edit your settings in a private chat with "
                          "the bot."))
        return

    us = UserSetting.get(id=update.message.from_user.id)

    if not us:
        us = UserSetting(id=update.message.from_user.id)

    if not us.stats:
        stats = '📊' + ' ' + _("Enable statistics")
    else:
        stats = '❌' + ' ' + _("Delete all statistics")

    kb = [[stats], ['🌍' + ' ' + _("Language")]]
    send_async(bot, chat.id, text='🔧' + ' ' + _("Settings"),
               reply_markup=ReplyKeyboardMarkup(keyboard=kb,
                                                one_time_keyboard=True))


@user_locale
def kb_select(bot, update, groups):
    chat = update.message.chat
    user = update.message.from_user
    option = groups[0]

    if option == '📊':
        us = UserSetting.get(id=user.id)
        us.stats = True
        send_async(bot, chat.id, text=_("Enabled statistics!"))

    elif option == '🌍':
        kb = [[locale + ' - ' + descr]
              for locale, descr
              in sorted(available_locales.items())]
        send_async(bot, chat.id, text=_("Select locale"),
                   reply_markup=ReplyKeyboardMarkup(keyboard=kb,
                                                    one_time_keyboard=True))

    elif option == '❌':
        us = UserSetting.get(id=user.id)
        us.stats = False
        us.first_places = 0
        us.games_played = 0
        us.cards_played = 0
        send_async(bot, chat.id, text=_("Deleted and disabled statistics!"))


@user_locale
def locale_select(bot, update, groups):
    chat = update.message.chat
    user = update.message.from_user
    option = groups[0]

    if option in available_locales:
        us = UserSetting.get(id=user.id)
        us.lang = option
        _.push(option)
        send_async(bot, chat.id, text=_("Set locale!"))
        _.pop()


def register():
    dispatcher.add_handler(CommandHandler('settings', show_settings))
    dispatcher.add_handler(RegexHandler('^([' + '📊' +
                                        '🌍' +
                                        '❌' + ']) .+$',
                                        kb_select, pass_groups=True))
    dispatcher.add_handler(RegexHandler(r'^(\w\w_\w\w) - .*',
                                        locale_select, pass_groups=True))