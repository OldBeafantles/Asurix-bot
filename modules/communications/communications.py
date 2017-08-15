import os
import requests
import discord
from ..utils import utils
from discord.ext import commands




class Communications:
    """Inter-channels communications module"""


    def parseCommunications(self):
        
        for conv in self.communications:
            for c in conv:
                
                channel = discord.utils.find(lambda x: x.id == c, self.bot.get_all_channels())
                
                if channel:
                    perms = channel.permissions_for(discord.utils.find(lambda m: m.id == self.bot.user.id, channel.server.members))
                    
                    if not perms.read_messages:
                        print("Warning: Can't read messages in #" + channel.name + ", in server " + channel.server.name)

                    if not perms.send_messages:
                        print("Warning: Can't send messages in #" + channel.name + ", in server " + channel.server.name)

                    if not perms.attach_files:
                        print("Warning: Can't attach files in #" + channel.name + ", in server " + channel.server.name)

                else:
                    print("Warning : There's no channel with " + c + " as ID! Please ensure the bot is in the server!")


    def loadCommunicationsFile(self):
        
        if not os.path.exists("modules/communications/data/communications.json"):
            
            if not os.path.isdir("modules/communications/data"):
                os.makedirs("modules/communications/data")
            
            jsonData = []
            utils.save_json(jsonData, "modules/communications/data/communications.json")
        
        self.communications = utils.load_json("modules/communications/data/communications.json")
        self.parseCommunications()

    def __init__(self, bot):
        
        # On charge les différentes communications voulues    
        self.bot = bot
        self.loadCommunicationsFile()
        self.attachmentsEmojis =        {
                                            "audio" : ":headphones:",
                                            "executable" : ":cd:",
                                            "image" : ":mountain:",
                                            "video" : ":tv:",
                                            "pdf" : ":closed_book:",
                                            "text_files" : ":pencil:",
                                            "others" : ":page_facing_up:"
                                        }

        self.attachmentsExtensions =    {
                                            "audio" : [".aa", ".aac", ".aax", ".act", ".aiff", ".amr", ".ape", ".au", ".awb", ".dct", ".dss", ".dvf", ".flac", ".gsm", ".iklax", ".ivs", ".m4a", ".m4b", ".mmf", ".mp3", ".mpc", ".msv", ".ogg", ".oga", ".mogg", ".opus", ".ra", ".raw", ".sln", ".tta", ".vox", ".wav", ".wma", ".wv", ".8svx"],
                                            "video" : [".webm", ".mkv", ".flv", ".vob", ".ogv", ".ogg", ".drc", ".gifv", ".mng", ".avi", ".mov", ".qt", ".wmv", ".yuv", ".rm", ".rmvb", ".asf", ".amv", ".mp4", ".m4p", ".m4v", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".m2v", ".svi", ".3gp", ".3g2", ".mxf", ".roq", ".nsv", ".f4v", ".f4p", ".f4a", ".f4b"],
                                            "executable" : [".exe", ".bat", ".sh"],
                                            "image" : [".ani", ".bmp", ".cal", ".fax", ".gif", ".img", ".jbg", ".jpe", ".jpeg", ".jpg", ".mac", ".pbm", ".pcd", ".pcx", ".pct", ".pgm", ".png", ".ppm", ".psd", ".ras", ".tga", ".tiff", ".wmf"],
                                            "pdf" : [".pdf"],
                                            "text_files" : [".dot", ".txt", ".docx", ".dotx", ".epub", ".odt", ".ott", ".odm", ".md"]
                                        }      


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
                embedMsg = discord.Embed(type = "rich", description = msg.content, colour = color)

                embedMsg.set_footer(text = "In #" + msg.channel.name + " (server: " + msg.server.name + ")", icon_url = msg.server.icon_url)
                embedMsg.set_author(name = msg.author.name + "#" + msg.author.discriminator, url = msg.author.avatar_url, icon_url = msg.author.avatar_url)
                
                if len(msg.attachments) != 0:
                    i = 1
                    for a in msg.attachments:
                        emote = None
                        extension = a["filename"][a["filename"].rfind("."):]
                        for e in self.attachmentsExtensions:
                            if extension in self.attachmentsExtensions[e]:
                                emote = self.attachmentsEmojis[e]
                                break
                        if not emote:
                            emote = self.attachmentsEmojis["others"]
                        embedMsg.add_field(name = "Attachment #" + str(i), value = emote + " [" + a["filename"] + "](" + a["url"] + ")", inline = False)
                        i += 1

                for c in self.communications:
                    if msg.channel.id in c:
                        for channel in c:
                            if channel != msg.channel.id:
                                
                                channelToSend = discord.utils.find(lambda c: c.id == channel, self.bot.get_all_channels())
                                if channelToSend:
                                    await self.bot.send_message(channelToSend, embed = embedMsg)



def setup(bot):
    mod = Communications(bot)
    bot.add_listener(mod.checkCommunications, "on_message")
    bot.add_cog(mod)