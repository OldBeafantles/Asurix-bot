"""Asurix-bot file"""

import os
import sys
import importlib

from datetime import datetime, timedelta
import discord
from discord.ext import commands
from modules.utils import utils

# Useful functions
if sys.platform == "win32" or sys.platform == "win64":
    CLEAR = lambda: os.system("cls")
else:
    CLEAR = lambda: os.system("clear")


class AsurixBot(commands.Bot):
    """The bot class"""
    # pylint: disable=too-many-instance-attributes
    def load_config(self):
        """Loads self.config_file_path, gets the infos if the file doesn't exists"""
        # Premier lancement du bot ou édition manuelle de l'utilisateur
        if not os.path.exists(self.config_file_path):

            json_data = {}
            token = input("Please put your bot's token here:\n> ")
            print("DO NOT SPREAD YOUR bot'S TOKEN TO ANYONE. NEVER.\n")
            prefix = input("\n\nPlease put your bot's prefix here:\n> ")
            description = input("\n\nPlease put a little description for your bot (optionnal)\n> ")
            if description == "":
                description = "A basic bot originally made for Asurix#4727"
            owner_id = input("\n\nPlease put your ID:\n> ")

            json_data["token"] = token
            json_data["prefix"] = prefix
            json_data["description"] = description
            json_data["owner id"] = owner_id
            self.token = token
            self.prefix = prefix
            self.description = description
            self.owner_id = owner_id

            if not os.path.isdir("settings"):
                os.makedirs("settings")

            utils.save_json(json_data, self.config_file_path)

        else:
            json_data = utils.load_json(self.config_file_path)
            if not "token" in json_data or not "prefix" in json_data \
            or not "description" in json_data or not "owner id" in json_data:
                print("\"settings/config.json\" is incorrect! The bot will be reseted, " \
                        + "please restart the bot!")
                os.remove(self.config_file_path)
                sys.exit(1)
            else:
                self.token = json_data["token"]
                self.prefix = json_data["prefix"]
                self.description = json_data["description"]
                self.owner_id = json_data["owner id"]


    def reset_infos(self):
        """Resets bot's info"""
        json_data = {}
        json_data["created at"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        json_data["total commands"] = 0
        json_data["total runtime"] = 0
        self.created_at = datetime.now()
        self.total_commands = 0
        self.total_runtime = timedelta(seconds=0)

        # Ne devrait pas être nécessaire étant donné que load_config
        # est appelé juste avant mais on ne sait jamais...
        if not os.path.isdir("settings"):
            os.makedirs("settings")

        utils.save_json(json_data, self.info_file_path)

    def load_infos(self):
        """Load bot's info"""
        # Premier lancement du bot ou édition manuelle de l'utilisateur
        if not os.path.exists(self.info_file_path):
            self.reset_infos()
        else:
            json_data = utils.load_json(self.info_file_path)
            if not "created at" in json_data or not "total commands" in json_data \
                                            or not "total runtime" in json_data:
                print("\"settings/infos.json\" is incorrect! The info of " + \
                    "the bot will be reseted!")
                self.reset_infos()
            else:
                self.created_at = datetime.strptime(json_data["created at"], "%d/%m/%Y %H:%M:%S")
                self.total_commands = json_data["total commands"]
                self.total_runtime = timedelta(seconds=json_data["total runtime"])

    def load_blacklist(self):
        """Loads the blacklist"""
        if not os.path.exists(self.blacklist_file_path):
            if not os.path.isdir("settings"):
                os.makedirs("settings")

            utils.save_json(self.blacklist, self.blacklist_file_path)
        else:
            self.blacklist = utils.load_json(self.blacklist_file_path)


    def load_modules(self):
        """Loads the bot modules"""
        # Première lancement du bot ou édition manuelle de l'utilisateur
        if not os.path.exists(self.modules_file_path):
            json_data = self.default_modules
            self.modules = self.default_modules
            utils.save_json(json_data, self.modules_file_path)

        print("\n\n")
        self.modules = utils.load_json(self.modules_file_path)
        to_remove = []
        for mod in self.modules:
            module_path = "modules/" + mod + ".py"
            module_name = module_path.replace('/', '.')[:-3]
            if not os.path.exists(module_path):
                print("\n\nThe module \"" + mod + "\" doesn't exist!")
                to_remove.append(mod)
            else:
                try:
                    print("Loading " + mod + " module...")
                    module = importlib.import_module(module_path.replace('/', '.')[:-3])
                    importlib.reload(module)
                    super().load_extension(module_name)
                    self.loaded_modules.append(mod)
                except SyntaxError as ex:
                    print("Error in " + mod + " module:\n\n" + str(ex) + "\n\n")
                    to_remove.append(mod)
        for mod in to_remove:
            self.modules.remove(mod)
        if to_remove:
            utils.save_json(self.modules, self.modules_file_path)


    def __init__(self, loop):

        CLEAR()
        self.token = ""
        self.prefix = ""
        self.description = ""
        self.owner_id = ""
        self.config_file_path = "settings/config.json"
        self.load_config()
        self.created_at = None
        self.total_commands = 0
        self.total_runtime = None
        self.info_file_path = "settings/infos.json"
        self.load_infos()
        self.bot = discord.Client()
        self.default_modules = ["base", "admin"]
        self.loaded_modules = []
        self.modules_file_path = "settings/modules.json"
        self.blacklist_file_path = "settings/blacklist.json"
        self.blacklist = []
        self.load_blacklist()
        self.invite_link = ""
        self.modules = []
        self.version = "0.0.1"
        self.launched_at = datetime.now()
        super().__init__(command_prefix=self.prefix, description=self.description, loop=loop)

        CLEAR()
