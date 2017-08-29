"""Runs bot"""

import logging
import sys
import asyncio
from datetime import datetime
import discord
from bot_asurix import AsurixBot
from modules.utils import utils

def run_bot():
    """Runs the bot"""

    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename="discord.log", encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
    logger.addHandler(handler)
    loop = asyncio.new_event_loop()
    asyncio.get_event_loop()

    bot = AsurixBot(loop)

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
    async def on_command(command, ctx):
        """Triggers AFTER a command is called"""
        #pylint: disable=unused-argument
        #pylint: disable=unused-variable
        bot.total_commands += 1

    @bot.event
    async def on_message(message):
        #pylint: disable=unused-variable
        """Triggers when the bot reads a new message"""
        if message.author.id not in bot.blacklist:
            await bot.process_commands(message)

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
