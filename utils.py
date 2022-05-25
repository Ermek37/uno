import logging

from telegram.ext.dispatcher import run_async

from internationalization import _, __
from mwt import MWT
from shared_vars import gm

logger = logging.getLogger(__name__)

TIMEOUT = 2.5


def list_subtract(list1, list2):
    list1 = list1.copy()

    for x in list2:
        list1.remove(x)

    return list(sorted(list1))

def display_name(user):
    user_name = user.first_name
    if user.username:
        user_name += ' (@' + user.username + ')'
    return user_name

def display_color(color):
    if color == "r":
        return _("{emoji} Red").format(emoji='❤️')
    if color == "b":
        return _("{emoji} Blue").format(emoji='💙')
    if color == "g":
        return _("{emoji} Green").format(emoji='💚')
    if color == "y":
        return _("{emoji} Yellow").format(emoji='💛')

def display_color_group(color, game):
    if color == "r":
        return __("{emoji} Red", game.translate).format(
            emoji='❤️')
    if color == "b":
        return __("{emoji} Blue", game.translate).format(
            emoji='💙')
    if color == "g":
        return __("{emoji} Green", game.translate).format(
            emoji='💚')
    if color == "y":
        return __("{emoji} Yellow", game.translate).format(
            emoji='💛')