from pony.orm import Optional, PrimaryKey
from database import db


class UserSetting(db.Entity):

    id = PrimaryKey(int, auto=False, size=64)  
    lang = Optional(str, default='')  
    stats = Optional(bool, default=False)  
    first_places = Optional(int, default=0)  
    games_played = Optional(int, default=0)  
    cards_played = Optional(int, default=0) 
    use_keyboards = Optional(bool, default=False)  