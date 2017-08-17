import os
import requests
import discord
from .utils import utils
from discord.ext import commands



class Communications:
    """Inter-channels communications module"""


    def parseCommunications(self):
        
        for conv in self.communications:
            for c in conv["channels"]:
                
                channel = discord.utils.find(lambda x: x.id == c, self.bot.get_all_channels())

                if channel:
                    perms = channel.permissions_for(discord.utils.find(lambda m: m.id == self.bot.user.id, channel.server.members))
                    
                    if not perms.read_messages:
                        print("Warning: Can't read messages in #" + channel.name + ", in server " + channel.server.name)

                    if not perms.send_messages:
                        print("Warning: Can't send messages in #" + channel.name + ", in server " + channel.server.name)

                else:
                    print("Warning : I don't have access to the channel with " + c + " as ID! Please ensure the channel exists and that the bot is in the server and have \"Read message\" permission in this channel!")


    def loadCommunicationsFile(self):
        
        if not os.path.exists("data/communications/communications.json"):
            
            if not os.path.isdir("data/communications"):
                os.makedirs("data/communications")
            
            jsonData = []
            utils.save_json(jsonData, "data/communications/communications.json")
        
        self.communications = utils.load_json("data/communications/communications.json")
        self.parseCommunications()

    def __init__(self, bot):
        
        # On charge les différentes communications voulues    
        self.bot = bot
        self.ownerID = bot.ownerID
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
            for channel in c["channels"]:
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
                    image = False
                    for a in msg.attachments:
                        emote = None
                        extension = a["filename"][a["filename"].rfind("."):]
                        if extension in self.attachmentsExtensions["image"] and not image:
                            image = True
                            embedMsg.set_image(url = a["url"])
                        else:
                            for e in self.attachmentsExtensions:
                                if extension in self.attachmentsExtensions[e]:
                                    emote = self.attachmentsEmojis[e]
                                    break
                            if not emote:
                                emote = self.attachmentsEmojis["others"]
                            embedMsg.add_field(name = "Attachment #" + str(i), value = emote + " [" + a["filename"] + "](" + a["url"] + ")", inline = False)
                            i += 1

                for c in self.communications:
                    if msg.channel.id in c["channels"]:
                        for channel in c["channels"]:
                            if channel != msg.channel.id:
                                
                                channelToSend = discord.utils.find(lambda c: c.id == channel, self.bot.get_all_channels())
                                if channelToSend:
                                    await self.bot.send_message(channelToSend, embed = embedMsg)

    
    
    async def checkChannelsDeletions(self, channel):
        owner = discord.utils.find(lambda u: u.id == self.ownerID, self.bot.get_all_members())
        if owner:
            for conv in self.communications:
                if channel.id in conv["channels"]:
                    await self.bot.send_message(owner, ":warning: The channel \"" + channel.name + "\" in the server \"" + channel.server.name + "\" has been deleted.\n:warning: The communication `" + conv["name"] + "` is affected by this change.\nYou can remove this channel from this communication using `rem_channel_com " + conv["name"] + " " + channel.id + "`!")
        else:
            print("The owner has no servers in common with the bot!")


    async def checkChannelsUpdates(self, before, after):
        for conv in self.communications:
            if after.id in conv["channels"]:
                perms = after.permissions_for(discord.utils.find(lambda m: m.id == self.bot.user.id, after.server.members))
                owner = discord.utils.find(lambda u: u.id == self.ownerID, self.bot.get_all_members())
                if owner:
                    if not perms.read_messages:
                        await self.bot.send_message(owner, ":warning: The channel \"" + after.name + "\" in the server \"" + after.server.name + "\" has been updated.\nI can't read messages there anymore!\nThe communication `" + conv["name"] + "` is affected by this change.")

                    if not perms.send_messages:
                        await self.bot.send_message(owner, ":warning: The channel \"" + after.name + "\" in the server \"" + after.server.name + "\" has been updated.\nI can't send messages there!\nThe communication `" + conv["name"] + "` is affected by this change.")
                else:
                    print("The owner has no servers in common with the bot!")


    async def checkRolesChanges(self, before, after):
        for conv in self.communications:
            for c in conv["channels"]:
                channel = discord.utils.find(lambda x: x.id == c, after.server.channels)
                if channel:
                    perms = channel.permissions_for(discord.utils.find(lambda m: m.id == self.bot.user.id, after.server.members))
                    owner = discord.utils.find(lambda u: u.id == self.ownerID, self.bot.get_all_members())
                    if owner:
                        if not perms.read_messages:
                            await self.bot.send_message(owner, ":warning: My permissions in the server \"" + after.server.name + "\" have been updated.\nI can't read messages in the channel \"" + channel.name + "\" anymore!\nThe communication `" + conv["name"] + "` is affected by this change.")

                        if not perms.send_messages:
                            await self.bot.send_message(owner, ":warning: My permissions in the server \"" + after.server.name + "\" have been updated.\nI can't send messages in the channel \"" + channel.name + "\"!\nThe communication `" + conv["name"] + "` is affected by this change.")
                    else:
                        print("The owner has no servers in common with the bot!")


    async def checkServersDeletes(self, server):
        for conv in self.communications:
            for c in conv["channels"]:
                channel = discord.utils.find(lambda x: x.id == c, server.channels)
                if channel:
                    owner = discord.utils.find(lambda o: o.id == self.ownerID, self.bot.get_all_members())
                    if owner:
                        await self.bot.send_message(owner, ":warning: I'm not in the server \"" + server.name + "\" anymore. I can't access to the channel " + channel.name + " anymore!\nThe communication `" + conv["name"] + "` is affected by this change.")
                    else:
                        print("The owner has no servers in common with the bot!")


    async def checkRolesDeletes(self, role):
        for conv in self.communications:
            for c in conv["channels"]:
                channel = discord.utils.find(lambda x: x.id == c, role.server.channels)
                if channel:
                    perms = channel.permissions_for(discord.utils.find(lambda m: m.id == self.bot.user.id, role.server.members))
                    owner = discord.utils.find(lambda u: u.id == self.ownerID, self.bot.get_all_members())
                    if owner:
                        if not perms.read_messages:
                            await self.bot.send_message(owner, ":warning: My permissions in the server \"" + role.server.name + "\" have been updated.\nI can't read messages in the channel \"" + channel.name + "\" anymore!\nThe communication `" + conv["name"] + "` is affected by this change.")

                        if not perms.send_messages:
                            await self.bot.send_message(owner, ":warning: My permissions in the server \"" + role.server.name + "\" have been updated.\nI can't send messages in the channel \"" + channel.name + "\"!\nThe communication `" + conv["name"] + "` is affected by this change.")
                    else:
                        print("The owner has no servers in common with the bot!")
    
    
    async def checkRolesUpdates(self, before, after):
        for conv in self.communications:
            for c in conv["channels"]:
                channel = discord.utils.find(lambda x: x.id == c, after.server.channels)
                if channel:
                    perms = channel.permissions_for(discord.utils.find(lambda m: m.id == self.bot.user.id, after.server.members))
                    owner = discord.utils.find(lambda u: u.id == self.ownerID, self.bot.get_all_members())
                    if owner:
                        if not perms.read_messages:
                            await self.bot.send_message(owner, ":warning: My permissions in the server \"" + after.server.name + "\" have been updated.\nI can't read messages in the channel \"" + channel.name + "\" anymore!\nThe communication `" + conv["name"] + "` is affected by this change.")

                        if not perms.send_messages:
                            await self.bot.send_message(owner, ":warning: My permissions in the server \"" + after.server.name + "\" have been updated.\nI can't send messages in the channel \"" + channel.name + "\"!\nThe communication `" + conv["name"] + "` is affected by this change.")
                    else:
                        print("The owner has no servers in common with the bot!")



def setup(bot):
    mod = Communications(bot)
    bot.add_listener(mod.checkCommunications, "on_message")
    bot.add_listener(mod.checkChannelsDeletions, "on_channel_delete")
    bot.add_listener(mod.checkChannelsUpdates, "on_channel_update")
    bot.add_listener(mod.checkRolesChanges, "on_member_update")
    bot.add_listener(mod.checkServersDeletes, "on_server_remove")
    bot.add_listener(mod.checkRolesDeletes, "on_server_role_delete")
    bot.add_listener(mod.checkRolesUpdates, "on_server_role_update")
    bot.add_cog(mod)