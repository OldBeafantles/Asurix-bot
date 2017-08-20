"""Asurix-bot file"""

import os
import logging
import sys
import importlib
import discord
from discord.ext import commands
from cogs.utils import utils

# Useful functions
if sys.platform == "win32" or sys.platform == "win64":
    CLEAR = lambda: os.system("cls")
else:
    CLEAR = lambda: os.system("clear")

# Logger
LOGGER = logging.getLogger('discord')
LOGGER.setLevel(logging.DEBUG)
HANDLER = logging.FileHandler(filename="discord.log", encoding='utf-8', mode='w')
HANDLER.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
LOGGER.addHandler(HANDLER)


class AsurixBot(commands.Bot):
    """The bot class"""
    # pylint: disable=too-many-instance-attributes
    def check_infos(self):
        """Loads "settings/infos.json", gets the infos if the file doesn't exists"""
        # Première lancement du bot ou édition manuelle de l'utilisateur
        if not os.path.exists("settings/infos.json"):

            json_data = {}
            token = input("Please put your bot's token here:\n> ")
            print("DO NOT SPREAD YOUR BOT'S TOKEN TO ANYONE. NEVER.\n")
            prefix = input("\n\nPlease put your bot's prefix here:\n> ")
            description = input("\n\nPlease put a little description for your bot (optionnal)\n> ")
            if description == "":
                description = "A basic bot originally made for Asurix#4727"
            owner_id = input("\n\nPlease put your ID:\n> ")

            json_data["token"] = token
            json_data["prefix"] = prefix
            json_data["description"] = description
            json_data["ownerID"] = owner_id
            self.token = token
            self.prefix = prefix
            self.description = description
            self.owner_id = owner_id

            if not os.path.isdir("settings"):
                os.makedirs("settings")

            utils.save_json(json_data, "settings/infos.json")

        else:
            json_data = utils.load_json("settings/infos.json")
            if not json_data["token"] or not json_data["prefix"] \
            or not json_data["description"] or not json_data["ownerID"]:
                print("\"settings/infos.json\" is incorrect! The bot will be reseted, " \
                        + "please restart the bot!")
                os.remove("settings/infos.json")
                sys.exit(1)
            else:
                self.token = json_data["token"]
                self.prefix = json_data["prefix"]
                self.description = json_data["description"]
                self.owner_id = json_data["ownerID"]


    def load_modules(self):
        """Loads the bot modules"""
        # Première lancement du bot ou édition manuelle de l'utilisateur
        if not os.path.exists("settings/cogs.json"):
            json_data = self.default_modules
            self.modules = self.default_modules
            utils.save_json(json_data, "settings/cogs.json")

        print("\n\n")
        self.modules = utils.load_json("settings/cogs.json")
        for mod in self.modules:
            module_path = "cogs/" + mod + ".py"
            module_name = module_path.replace('/', '.')[:-3]
            if not os.path.exists(module_path):
                print("\n\nThe cog \"" + mod + "\" doesn't exist!")
            else:
                try:
                    print("Loading " + mod + " module...")
                    module = importlib.import_module(module_path.replace('/', '.')[:-3])
                    importlib.reload(module)
                    super().load_extension(module_name)
                    self.loaded_modules.append(mod)
                except SyntaxError as ex:
                    print("Error in " + mod + " module:\n\n" + str(ex) + "\n\n")
                    continue


    def run(self, *args, **kwargs):
        """Runs the bot"""
        try:
            super().run(self.token, reconnect=True)
        except discord.LoginFailure:
            print("Couldn't log in, your bot's token might be incorrect! If it's not, "\
                    + "then check Discord's status here: https://status.discordapp.com/")
            answer = input("Do you want to change your bot's token? (yes/no)\n> ")
            if answer.upper() == "YES":
                token = input("\n\nPlease put your new bot's token here:\n> ")
                json_data = utils.load_json("settings/infos.json")
                json_data["token"] = token
                self.token = token
                utils.save_json(json_data, "settings/infos.json")
                sys.exit(1)
        except discord.GatewayNotFound:
            print("Gateway not found! The problem comes from Discord.")
            sys.exit(1)
        except discord.ConnectionClosed:
            print("No more connection.")
            sys.exit(1)
        except discord.HTTPException:
            print("HTTP Error.")
            sys.exit(1)


    def __init__(self):

        CLEAR()
        self.token = ""
        self.prefix = ""
        self.description = ""
        self.owner_id = ""
        self.check_infos()
        self.bot = discord.Client()
        self.default_modules = ["communications", "owner"]
        self.loaded_modules = []
        self.invite_link = ""
        self.modules = []
        super().__init__(command_prefix=self.prefix, description=self.description)

        CLEAR()


    def is_owner(self, userid: str):
        """Returns true if the id provided is the owner id"""
        return userid == self.owner_id


BOT = AsurixBot()

@BOT.event
async def on_ready():
    """Triggers when the bot just logged in"""
    print("Logged in as " + BOT.user.name + "#" + BOT.user.discriminator)
    print(str(len(BOT.servers))+ " servers")
    print(str(len(set(BOT.get_all_channels()))) + " channels")
    print(str(len(set(BOT.get_all_members()))) + " members")
    BOT.invite_link = "https://discordapp.com/oauth2/authorize?client_id=" \
                        + BOT.user.id + "&scope=bot"
    print("\nHere's the invitation link for your bot: " + BOT.invite_link)
    BOT.load_modules()
    print("\n" + str(len(BOT.loaded_modules)) + " modules loaded.")

BOT.run()
