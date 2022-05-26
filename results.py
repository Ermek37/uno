
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, \
    InlineQueryResultCachedSticker as Sticker

import card as c
from utils import display_color, display_color_group, display_name
from internationalization import _, __


def add_choose_color(results, game):
    for color in c.COLORS:
        results.append(
            InlineQueryResultArticle(
                id=color,
                title=_("Choose Color"),
                description=display_color(color),
                input_message_content=
                InputTextMessageContent(display_color_group(color, game))
            )
        )
