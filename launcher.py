"""The launcher for the bot"""

import os
import subprocess
import sys
import logging
import asyncio
from datetime import datetime
import discord
from bot_asurix import AsurixBot
from modules.utils import utils

# pylint: disable=exec-used
# USEFUL FUNCTIONS
if sys.platform == "win32" or sys.platform == "win64":
    CLEAR = lambda: os.system("cls")
else:
    CLEAR = lambda: os.system("clear")


def run_bot():
    """Runs the bot"""

    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename="discord.log", encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
    logger.addHandler(handler)
    bot = AsurixBot()

    @bot.event
    async def on_ready():
        """Triggers when the bot just logged in"""
        #pylint: disable=unused-variable
        print("Logged in as " + bot.user.name + "#" + bot.user.discriminator)
        print(str(len(bot.servers))+ " servers")
        print(str(len(set(bot.get_all_channels()))) + " channels")
        print(str(len(set(bot.get_all_members()))) + " members")
        bot.invite_link = "https://discordapp.com/oauth2/authorize?client_id=" \
                            + bot.user.id + "&scope=bot"
        print("\nHere's the invitation link for your bot: " + bot.invite_link)
        bot.load_modules()
        bot.launched_at = datetime.now()
        print("\n" + str(len(bot.loaded_modules)) + " modules loaded.")

    @bot.event
    async def on_command(self, message):
        """Triggers AFTER a command is called"""
        #pylint: disable=unused-argument
        #pylint: disable=unused-variable
        bot.total_commands += 1

    loop = asyncio.new_event_loop()
    asyncio.get_event_loop()
    try:
        loop.run_until_complete(bot.run(bot.token, reconnect=True))
    except discord.LoginFailure:
        print("Couldn't log in, your bot's token might be incorrect! If it's not, "\
                + "then check Discord's status here: https://status.discordapp.com/")
        answer = input("Do you want to change your bot's token? (yes/no)\n> ")
        if answer.upper() == "YES":
            token = input("\n\nPlease put your new bot's token here:\n> ")
            json_data = utils.load_json("settings/infos.json")
            json_data["token"] = token
            bot.token = token
            utils.save_json(json_data, "settings/infos.json")
    except KeyboardInterrupt:
        loop.run_util_complete(bot.close())
    except discord.GatewayNotFound:
        print("Gateway not found! The problem comes from Discord.")
        sys.exit(1)
    except discord.ConnectionClosed:
        print("No more connection.")
        loop.run_util_complete(bot.close())
        sys.exit(1)
    except discord.HTTPException:
        print("HTTP Error.")
        sys.exit(1)
    finally:
        loop.close()


def install_update():
    """Installs/Updates the requirements"""

    os.system("pip install --upgrade pip")

    #Get the requirements
    file = open("requirements.txt", "r")
    requirements = file.readlines()
    file.close()

    # Update the requirements
    for req in requirements:
        os.system(req)



# LAUNCHING THE BOT
CLEAR()

subprocess.call("git fetch", stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT, shell=True)
RESULT = subprocess.check_output("git status", shell=True)
if "Your branch is behind" in str(RESULT):
    ANSWER = input("The bot isn't up-to-date, please type 'yes' to update it!\n\n> ")
    if ANSWER.upper() == "YES":
        os.system("git pull")

ANSWER = ""
while ANSWER != "3":
    CLEAR()

    ANSWER = input("What do you want to do?\n\n" + \
                   "1. Install & update requirements\n" + \
                   "2. Launch the bot\n" + \
                   "3. Quit\n\n> ")

    if ANSWER == "1":
        install_update()
    elif ANSWER == "2":
        run_bot()
