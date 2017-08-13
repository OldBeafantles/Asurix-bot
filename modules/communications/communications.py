import os
import requests
import discord
from io import BytesIO
from ..utils import utils



class Communications:
    """Inter-channels communications module"""

    def loadCommunicationsFile(self):
        
        if not os.path.exists("modules/communications/data/communications.json"):
            
            if not os.path.isdir("modules/communications/data"):
                os.makedirs("modules/communications/data")
            
            jsonData = []
            utils.save_json(jsonData, "modules/communications/data/communications.json")
        
        self.communications = utils.load_json("modules/communications/data/communications.json")

    def __init__(self, bot):
        
        # On charge les différentes communications voulues    
        self.bot = bot
        self.loadCommunicationsFile()


    def isConcerned(self, channelID : str):
        for c in self.communications:
            for channel in c:
                if channel == channelID:
                    return True
        return False

    async def checkCommunications(self, msg):

        if msg.author.id != self.bot.user.id:
            if self.isConcerned(msg.channel.id):
                
                color = discord.Colour(sorted(msg.author.roles, key = lambda r: r.position, reverse=True)[0].colour.value)

                embedsToSend = []
                attachmentsToSend = []

                if not ((len(msg.embeds) != 0 and sum(len(i["url"]) for i in msg.embeds) + msg.content.count(" ") == len(msg.content)) or (len(msg.content) == 0 and len(msg.attachments) != 0)):
                    embedMsg = discord.Embed(description = msg.content, colour = color)
                    embedMsg.set_author(name = msg.author.name + "#" + msg.author.discriminator, icon_url = msg.author.avatar_url)

                
                if len(msg.embeds) != 0:
                    for e in msg.embeds:
                        embedsToSend.append("`From " + msg.author.name + "#" + msg.author.discriminator + ":\n\n`" + e["url"])

                if len(msg.attachments) != 0:
                    for a in msg.attachments:
                        r = requests.get(a["url"])
                        if r.status_code == 200:
                            attachmentsToSend.append([BytesIO(r.content), a["filename"], "`From " + msg.author.name + "#" + msg.author.discriminator + "`:"])
                
                for c in self.communications:
                    if msg.channel.id in c:
                        for channel in c:
                            if channel != msg.channel.id:
                                
                                channelToSend = discord.utils.find(lambda c: c.id == channel, self.bot.get_all_channels())
                                if channelToSend:
                                    
                                    if embedMsg:
                                        await self.bot.send_message(channelToSend, embed = embedMsg)

                                    for e in embedsToSend:
                                        await self.bot.send_message(channelToSend, content = e)

                                    for a in attachmentsToSend:
                                        await self.bot.send_file(destination = channelToSend, fp = a[0], filename = a[1], content = a[2])





def setup(bot):
    mod = Communications(bot)
    bot.add_listener(mod.checkCommunications, "on_message")
    bot.add_cog(mod)