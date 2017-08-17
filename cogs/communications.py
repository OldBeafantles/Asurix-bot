import os
import requests
import discord
from .utils import utils
from .utils import checks
from discord.ext import commands



class Communications:
    """Inter-channels communications module"""


    def parseCommunications(self):
        
        for conv in self.communications:
            for c in self.communications[conv]:
                
                channel = discord.utils.find(lambda x: x.id == c, self.bot.get_all_channels())

                if channel:
                    perms = channel.permissions_for(discord.utils.find(lambda m: m.id == self.bot.user.id, channel.server.members))
                    
                    if not perms.read_messages:
                        print("Warning: Can't read messages in #" + channel.name + ", in server " + channel.server.name)

                    if not perms.send_messages:
                        print("Warning: Can't send messages in #" + channel.name + ", in server " + channel.server.name)

                else:
                    print("Warning : I don't have access to the channel with " + c + " as ID! Please ensure the channel exists and that the bot is in the server and have \"Read message\" + \"Send messages\" permissions in this channel!")


    def loadCommunicationsFile(self):
        
        if not os.path.exists("data/communications/communications.json"):
            
            if not os.path.isdir("data/communications"):
                os.makedirs("data/communications")
            
            jsonData = {}
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
            for channel in self.communications[c]:
                if channel == channelID:
                    return True
        return False


    @commands.command(pass_context = True)
    @checks.is_owner()
    async def add_conv(self, ctx, convName : str, *channels):
        """Adds a conversation
        Parameters:
            convName: The name you want to use for the conversation (no spaces).
            *channels: The list of the channels IDs for the conversation, separated by spaces.

        Example: [p]add_conv myFirstConv 347571375466086401 346323687554809857 345548753366810625"""

        if convName not in self.communications:

            for c in channels:
                channel = discord.utils.find(lambda x: x.id == c, self.bot.get_all_channels())
                if channel:
                    
                    perms = channel.permissions_for(discord.utils.find(lambda m: m.id == self.bot.user.id, channel.server.members))
                        
                    if not perms.read_messages:
                        await self.bot.say(":warning: Can't read messages in #" + channel.name + ", in server " + channel.server.name)

                    if not perms.send_messages:
                        await self.bot.say(":warning: Can't send messages in #" + channel.name + ", in server " + channel.server.name)

                else:
                    await self.bot.say(":warning: I don't have access to the channel with " + c + " as ID! Please ensure the channel exists and that the bot is in the server and have `Read message` + `Send messages` permissions in this channel!")
            
            self.communications[convName] = [x for x in channels]
            utils.save_json(self.communications, "data/communications/communications.json")
            await self.bot.say("Conversation added! :ok_hand:")

        else:
            await self.bot.say("A conversation with this name already exists! Please choose another name, or edit the existing conversation!")


    @commands.command(pass_context = True)
    @checks.is_owner()
    async def rem_conv(self, ctx, convName : str):
        """Removes a conversation
        Parameters:
            convName: The name of the conversation you want to remove.
        
        Example: [p]rem_conv myFirstConv"""
        if convName in self.communications:
            del self.communications[convName]
            utils.save_json(self.communications, "data/communications/communications.json")
            await self.bot.say("The conversation `" + convName + "` has been removed. :ok_hand:")
        else:
            await self.bot.say("There's no conversation with such name. To get the list of the conversation, type `[p]list_conv`.")


    @commands.command(pass_context = True)
    @checks.is_owner()
    async def list_conv(self, ctx):
        """Lists all the conversations"""
        if len(self.communications) != 0:
            msg = "```Markdown\nList of the conversations\n========================\n\n"
            i = 1
            for c in self.communications:
                msg += "[" + str(i) + "](" + c + ")\n"
                i += 1
            msg += "```\nIf you want more details about a specific conversations, type `[p]get_conv_details convName`."
            await self.bot.say(msg)
        else:
            await self.bot.say("There's no conversations! :grimacing:")

    @commands.command(pass_context = True)
    @checks.is_owner()
    async def get_conv_details(self, ctx, convName : str):
        """Shows all the details about a conversation
        Parameters:
            convName: The name of the conversation you want the details.

        Example: [p]get_conv_details myFirstConv"""
        if convName in self.communications:
            msg = "Details for `" + convName + "`:\n\nChannels:\n---------------\n\n"
            i = 1
            for c in self.communications[convName]:
                msg += "\t" + str(i) + ") "
                channel = discord.utils.find(lambda x: x.id == c, self.bot.get_all_channels())
                if channel:
                    msg += channel.name + " (in server " + channel.server.name + ")\n"

                    perms = channel.permissions_for(discord.utils.find(lambda m: m.id == self.bot.user.id, channel.server.members))
                        
                    msg += "\t\tRead messages: "
                    if not perms.read_messages:
                        msg += ":x:"
                    else:
                        msg += ":white_check_mark:"

                    msg += "\n\t\tSend messages: "
                    if not perms.send_messages:
                        msg += ":x:"
                    else:
                        msg += ":white_check_mark:"

                else:
                    msg += "`UNKNOWN CHANNEL`"

                msg += "\n"
                i += 1

            await self.bot.say(msg)
        else:
            await self.bot.say("There's no conversation with such name. To get the list of the conversation, type `[p]list_conv`.")


    @commands.command(pass_context = True)
    @checks.is_owner()
    async def add_channels_conv(self, ctx, convName : str, *channels):
        """Adds channels to a conversation
        Parameters:
            convName: The name of the conversation you want to add channels to.
            channels: The list of the channels IDs you want to add, separated by spaces.

        Example:    [p]add_channels_conv myFirstConv 347571375466086401 346323687554809857 345548753366810625
                    [p]add_channels_conv myFirstConv 347571375466086401"""
        if convName in self.communications:
            msg = ""
            for c in channels:
                if c not in self.communications[convName]:
                    channel = discord.utils.find(lambda x: x.id == c, self.bot.get_all_channels())
                    if channel:
                        perms = channel.permissions_for(discord.utils.find(lambda m: m.id == self.bot.user.id, channel.server.members))
                        if not perms.read_messages:
                            msg += ":warning: Cant't read messages in " + channel.name + " (server: " + channel.server.name + ").\n"
                        if not perms.send_messages:
                            msg += ":warning: Cant't send messages in " + channel.name + " (server: " + channel.server.name + ").\n"
                    else:
                        msg += ":warning: I don't have access to the channel with " + c + " as ID! Please ensure the channel exists and that the bot is in the server and have \"Read message\" + \"Send messages\" permissions in this channel!\n"
                    self.communications[convName].append(c)
                else:
                    msg += c + " is already registered in this conversation.\n"
            utils.save_json(self.communications, "data/communications/communications.json")
            msg += "The channels have been added to the conversation `" + convName + "`."
            await self.bot.say(msg)
        else:
            await self.bot.say("There's no conversation with such name. To get the list of the conversation, type `[p]list_conv`.")
        
    @commands.command(pass_context = True)
    @checks.is_owner()
    async def rem_channels_conv(self, ctx, convName : str, *channels):
        """Removes channels from a conversation
        Parameters:
            convName: The name of the conversation you want to remove channels from.
            channels: The list of the channels IDs you want to remove, separated by spaces.

        Example:    [p]rem_channels_conv myFirstConv 347571375466086401 346323687554809857 345548753366810625
                    [p]rem_channels_conv myFirstConv 347571375466086401"""
        if convName in self.communications:
            msg = ""
            for c in channels:
                if c in self.communications[convName]:
                    channel = discord.utils.find(lambda x: x.id == c, self.bot.get_all_channels())
                    if channel:
                        msg += "Channel #" + channel.name + " (server: " + channel.server.name + ") has been removed from the conversation.\n"
                    else:
                        msg += "Channel with " + c + " as ID has been removed from the conversation.\n"
                    self.communications[convName].remove(c)
                else:
                    msg += "There's no channel with " + c + " as ID in this conversation.\n"
            utils.save_json(self.communications, "data/communications/communications.json")
            msg += "\nDone! :ok_hand:"
            await self.bot.say(msg)
        else:
            await self.bot.say("There's no conversation with such name. To get the list of the conversation, type `[p]list_conv`.")


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
                    if msg.channel.id in self.communications[c]:
                        for channel in self.communications[c]:
                            if channel != msg.channel.id:
                                
                                channelToSend = discord.utils.find(lambda c: c.id == channel, self.bot.get_all_channels())
                                if channelToSend:
                                    try:
                                        await self.bot.send_message(channelToSend, embed = embedMsg)
                                    except discord.Forbidden:
                                        print("Can't send messages to #" + channelToSend.name + " (server: " + channelToSend.server.name + ")")
                                    except Exception as e:
                                        print(e)
    
    
    async def checkChannelsDeletions(self, channel):
        owner = discord.utils.find(lambda u: u.id == self.ownerID, self.bot.get_all_members())
        if owner:
            for conv in self.communications:
                if channel.id in self.communications[conv]:
                    await self.bot.send_message(owner, ":warning: The channel \"" + channel.name + "\" in the server \"" + channel.server.name + "\" has been deleted.\n:warning: The communication `" + conv + "` is affected by this change.\nYou can remove this channel from this communication using `rem_channel_conv " + conv + " " + channel.id + "`!")
        else:
            print("The owner has no servers in common with the bot!")


    async def checkChannelsUpdates(self, before, after):
        for conv in self.communications:
            if after.id in self.communications[conv]:
                perms = after.permissions_for(discord.utils.find(lambda m: m.id == self.bot.user.id, after.server.members))
                owner = discord.utils.find(lambda u: u.id == self.ownerID, self.bot.get_all_members())
                if owner:
                    if not perms.read_messages:
                        await self.bot.send_message(owner, ":warning: The channel \"" + after.name + "\" in the server \"" + after.server.name + "\" has been updated.\nI can't read messages there anymore!\nThe communication `" + conv + "` is affected by this change.")

                    if not perms.send_messages:
                        await self.bot.send_message(owner, ":warning: The channel \"" + after.name + "\" in the server \"" + after.server.name + "\" has been updated.\nI can't send messages there!\nThe communication `" + conv + "` is affected by this change.")
                else:
                    print("The owner has no servers in common with the bot!")


    async def checkRolesChanges(self, before, after):
        for conv in self.communications:
            for c in self.communications[conv]:
                channel = discord.utils.find(lambda x: x.id == c, after.server.channels)
                if channel:
                    perms = channel.permissions_for(discord.utils.find(lambda m: m.id == self.bot.user.id, after.server.members))
                    owner = discord.utils.find(lambda u: u.id == self.ownerID, self.bot.get_all_members())
                    if owner:
                        if not perms.read_messages:
                            await self.bot.send_message(owner, ":warning: My permissions in the server \"" + after.server.name + "\" have been updated.\nI can't read messages in the channel \"" + channel.name + "\" anymore!\nThe communication `" + conv + "` is affected by this change.")

                        if not perms.send_messages:
                            await self.bot.send_message(owner, ":warning: My permissions in the server \"" + after.server.name + "\" have been updated.\nI can't send messages in the channel \"" + channel.name + "\"!\nThe communication `" + conv + "` is affected by this change.")
                    else:
                        print("The owner has no servers in common with the bot!")


    async def checkServersDeletes(self, server):
        for conv in self.communications:
            for c in self.communications[conv]:
                channel = discord.utils.find(lambda x: x.id == c, server.channels)
                if channel:
                    owner = discord.utils.find(lambda o: o.id == self.ownerID, self.bot.get_all_members())
                    if owner:
                        await self.bot.send_message(owner, ":warning: I'm not in the server \"" + server.name + "\" anymore. I can't access to the channel " + channel.name + " anymore!\nThe communication `" + conv + "` is affected by this change.")
                    else:
                        print("The owner has no servers in common with the bot!")


    async def checkRolesDeletes(self, role):
        for conv in self.communications:
            for c in self.communications[conv]:
                channel = discord.utils.find(lambda x: x.id == c, role.server.channels)
                if channel:
                    perms = channel.permissions_for(discord.utils.find(lambda m: m.id == self.bot.user.id, role.server.members))
                    owner = discord.utils.find(lambda u: u.id == self.ownerID, self.bot.get_all_members())
                    if owner:
                        if not perms.read_messages:
                            await self.bot.send_message(owner, ":warning: My permissions in the server \"" + role.server.name + "\" have been updated.\nI can't read messages in the channel \"" + channel.name + "\" anymore!\nThe communication `" + conv + "` is affected by this change.")

                        if not perms.send_messages:
                            await self.bot.send_message(owner, ":warning: My permissions in the server \"" + role.server.name + "\" have been updated.\nI can't send messages in the channel \"" + channel.name + "\"!\nThe communication `" + conv + "` is affected by this change.")
                    else:
                        print("The owner has no servers in common with the bot!")
    
    
    async def checkRolesUpdates(self, before, after):
        for conv in self.communications:
            for c in self.communications[conv]:
                channel = discord.utils.find(lambda x: x.id == c, after.server.channels)
                if channel:
                    perms = channel.permissions_for(discord.utils.find(lambda m: m.id == self.bot.user.id, after.server.members))
                    owner = discord.utils.find(lambda u: u.id == self.ownerID, self.bot.get_all_members())
                    if owner:
                        if not perms.read_messages:
                            await self.bot.send_message(owner, ":warning: My permissions in the server \"" + after.server.name + "\" have been updated.\nI can't read messages in the channel \"" + channel.name + "\" anymore!\nThe communication `" + conv + "` is affected by this change.")

                        if not perms.send_messages:
                            await self.bot.send_message(owner, ":warning: My permissions in the server \"" + after.server.name + "\" have been updated.\nI can't send messages in the channel \"" + channel.name + "\"!\nThe communication `" + conv + "` is affected by this change.")
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