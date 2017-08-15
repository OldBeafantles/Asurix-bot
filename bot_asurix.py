import discord
from discord.ext import commands
import asyncio
from modules.utils import utils
import os
import logging
import sys
import importlib

# Useful functions
if sys.platform == "win32" or sys.platform == "win64":
    clear = lambda: os.system("cls")
else:
    clear = lambda: os.system("clear")

# Logger
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename = "discord.log", encoding = 'utf-8', mode = 'w')
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)


class Bot(commands.Bot):
    

    def checkInfos(self):
        
        # Première lancement du bot ou édition manuelle de l'utilisateur
        if not os.path.exists("settings/infos.json"):

            jsonData = {}
            token = input("Please put your bot's token here:\n> ")
            print("DO NOT SPREAD YOUR BOT'S TOKEN TO ANYONE. NEVER.\n")
            prefix = input("\n\nPlease put your bot's prefix here:\n> ")
            description = input("\n\nPlease put a little description for your bot (optionnal)\n> ")
            if description == "":
                description = "A basic bot originally made for Asurix#4727"
            ownerID = input("\n\nPlease put your ID:\n> ")
            
            jsonData["token"] = token
            jsonData["prefix"] = prefix
            jsonData["description"] = description
            jsonData["ownerID"] = ownerID
            self.token = token
            self.prefix = prefix
            self.description = description
            self.ownerID = ownerID

            if not os.path.isdir("settings"):
                os.makedirs("settings")

            utils.save_json(jsonData, "settings/infos.json")

        else:
            jsonData = utils.load_json("settings/infos.json")
            if not jsonData["token"] or not jsonData["prefix"] or not jsonData["description"] or not jsonData["ownerID"]:
                print("\"settings/infos.json\" is incorrect! The bot will be reseted, please restart the bot!")
                os.remove("settings/infos.json")
                sys.exit(1)
            else:
                self.token = jsonData["token"]
                self.prefix = jsonData["prefix"]
                self.description = jsonData["description"]
                self.ownerID = jsonData["ownerID"]


    def run(self):
        
            try:
                super().run(self.token)
            except Exception as e:
                print("Couldn't log in, your bot's token might be incorrect! If it's not, then check Discord's status here: https://status.discordapp.com/")
                answer = input("Do you want to change your bot's token? (yes/no)\n> ")
                if answer.upper() == "YES":
                    token = input("\n\nPlease put your new bot's token here:\n> ")
                    jsonData = utils.load_json("settings/infos.json")
                    jsonData["token"] = token
                    self.token = token
                    utils.save_json(jsonData, "settings/infos.json")
                    sys.exit(1)


    def loadModules(self):

        # Première lancement du bot ou édition manuelle de l'utilisateur
        if not os.path.exists("settings/modules.json"):
            jsonData = self.defaultModules
            self.modules = self.defaultModules
            utils.save_json(jsonData, "settings/modules.json")

        self.modules = utils.load_json("settings/modules.json")
        for m in self.modules:
            modulePath = "modules/" + m + "/" + m + ".py"
            moduleName = modulePath.replace('/', '.')[:-3]
            if not os.path.exists(modulePath):
                print("The cog \"" + m + "\" doesn't exist!")
            else:
                try:
                    module = importlib.import_module(modulePath.replace('/', '.')[:-3])
                    importlib.reload(module)
                    super().load_extension(moduleName)
                    self.loadedModules.append(m)
                except SyntaxError as e:
                    print("Error in " + m + " module:\n\n" + str(e) + "\n\n")
                


    def __init__(self):

        clear()
        self.checkInfos()
        self.bot = discord.Client()
        self.defaultModules = ["communications"]
        self.loadedModules = []
        self.inviteLink = ""
        super().__init__(command_prefix = self.prefix, description = self.description)

        clear()
        self.loadModules()




bot = Bot()

@bot.event
async def on_ready():
    print("Logged in as " + bot.user.name + "#" + bot.user.discriminator)
    print(str(len(bot.servers))+ " servers")
    print(str(len(set(bot.get_all_channels()))) + " channels")
    print(str(len(set(bot.get_all_members()))) + " members")
    print("\n" + str(len(bot.loadedModules)) + " modules loaded.")
    bot.inviteLink = "https://discordapp.com/oauth2/authorize?client_id=" + bot.user.id + "&scope=bot"




bot.run()