# UNO

Aelina Daniyar kyzy, Ermek Ilikeshova and Aizhamal Zhetigenova worked on this project
Telegram Bot that allows you to play the popular card game UNO via inline queries. 
The project was implemented using Python with various modules for efficient arrays, machine learning and GUIs. Q-learning agents are trained inside the game environment and the resulting model can be analyzed inside a graphical version of the game including AI and human players, as well as a naive baseline algorithm.

To run the bot, you will need:

    Python (tested with 3.4+)
    The python-telegram-bot module
    Pony ORM

Setup

    Get a bot token from @BotFather and change configurations in config.json.
    Convert all language files from .po files to .mo by executing the bash script compile.sh located in the locales folder. Another option is: find . -maxdepth 2 -type d -name 'LC_MESSAGES' -exec bash -c 'msgfmt {}/unobot.po -o {}/unobot.mo' \;.
    Use /setinline and /setinlinefeedback with BotFather for your bot.
    Use /setcommands and submit the list of commands in commandlist.txt
    Install requirements (using a virtualenv is recommended): pip install -r requirements.txt

You can change some gameplay parameters like turn times, minimum amount of players and default gamemode in config.json. Current gamemodes available: classic, fast and wild. Check the details with the /modes command.
Then run the bot with python3 bot.py.

