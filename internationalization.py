import gettext
from functools import wraps

from locales import available_locales
from pony.orm import db_session
from user_setting import UserSetting
from shared_vars import gm

GETTEXT_DOMAIN = 'unobot'
GETTEXT_DIR = 'locales'


class _Underscore(object):
    def __init__(self):
        self.translators = {
            locale: gettext.GNUTranslations(
                open(gettext.find(
                    GETTEXT_DOMAIN, GETTEXT_DIR, languages=[locale]
                ), 'rb')
            )
            for locale
            in available_locales.keys()
            if locale != 'en_US'  # No translation file for en_US
        }
        self.locale_stack = list()

    def push(self, locale):
        self.locale_stack.append(locale)

    def pop(self):
        if self.locale_stack:
            return self.locale_stack.pop()
        else:
            return None

def code(self):
        if self.locale_stack:
            return self.locale_stack[-1]
        else:
            return None

def __call__(self, singular, plural=None, n=1, locale=None):
        if not locale:
            locale = self.locale_stack[-1]

        if locale not in self.translators.keys():
            if n is 1:
                return singular
            else:
                return plural

        translator = self.translators[locale]

        if plural is None:
            return translator.gettext(singular)
        else:
            return translator.ngettext(singular, plural, n)

_ = _Underscore()