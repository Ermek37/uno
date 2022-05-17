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