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
