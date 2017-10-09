"""Communications module"""

import os
import discord
from discord.ext import commands
from modules.utils import checks
from modules.utils import utils



class Conversation:
    """A class representing an inter-channels communication"""
    # pylint: disable=too-few-public-methods
    def __init__(self, channels):
        self.channels = channels
        self.messages = []


class Communications:
    """Inter-channels communications module"""
    #pylint: disable=too-many-public-methods
    def save(self):
        """Saves self.communications in self.communications_file_path"""
        data = {}
        for com in self.communications:
            data[com] = self.communications[com].channels
        utils.save_json(data, self.communications_file_path)

    def parse_communications(self):
        """Checks if there's no problem with the stored communications"""
        for conv in self.communications:
            for com in self.communications[conv].channels:
                channel = discord.utils.find(lambda x, c=com: x.id == c, \
                                            self.bot.get_all_channels())

                if channel:
                    perms = channel.permissions_for(discord.utils.find( \
                        lambda m: m.id == self.bot.user.id, channel.server.members))

                    if not perms.read_messages:
                        print("Warning: Can't read messages in #" + channel.name + \
                                ", in server " + channel.server.name)

                    if not perms.send_messages:
                        print("Warning: Can't send messages in #" + channel.name + \
                                ", in server " + channel.server.name)

                else:
                    print("Warning : I don't have access to the channel with " + com + \
                            " as ID! Please ensure the channel exists and that the " + \
                            "bot is in the server and have \"Read message\" + " + \
                            "\"Send messages\" permissions in this channel!")


    def load_communications_file(self):
        """Loads self.communications_file_path in self.communications"""
        self.communications = {}
        if not os.path.exists(self.communications_file_path):

            if not os.path.isdir("data/communications"):
                os.makedirs("data/communications")

            utils.save_json(self.communications, self.communications_file_path)
        else:
            conv = utils.load_json(self.communications_file_path)
            for com in conv:
                self.communications[com] = Conversation(conv[com])
            self.parse_communications()

    def __init__(self, bot):

        self.bot = bot
        self.owner_id = bot.owner_id
        self.communications_file_path = "data/communications/communications.json"
        self.load_communications_file()
        self.attachments_emojis = {"audio" : ":headphones:", \
                                  "executable" : ":cd:", \
                                  "image" : ":mountain:", \
                                  "video" : ":tv:", \
                                  "pdf" : ":closed_book:", \
                                  "text_files" : ":pencil:", \
                                  "others" : ":page_facing_up:"}

        self.attachments_extensions = {"audio" : [".aa", ".aac", ".aax", ".act", ".aiff", ".amr", \
                                                ".ape", ".au", ".awb", ".dct", ".dss", ".dvf", \
                                                ".flac", ".gsm", ".iklax", ".ivs", ".m4a", ".m4b", \
                                                ".mmf", ".mp3", ".mpc", ".msv", ".ogg", ".oga", \
                                                ".mogg", ".opus", ".ra", ".raw", ".sln", ".tta", \
                                                ".vox", ".wav", ".wma", ".wv", ".8svx"], \
                                      "video" : [".webm", ".mkv", ".flv", ".vob", ".ogv", ".ogg", \
                                                ".drc", ".gifv", ".mng", ".avi", ".mov", ".qt", \
                                                ".wmv", ".yuv", ".rm", ".rmvb", ".asf", ".amv", \
                                                ".mp4", ".m4p", ".m4v", ".mpg", ".mp2", ".mpeg", \
                                                ".mpe", ".mpv", ".m2v", ".svi", ".3gp", ".3g2", \
                                                ".mxf", ".roq", ".nsv", ".f4v", ".f4p", ".f4a", \
                                                ".f4b"], \
                                      "executable" : [".exe", ".bat", ".sh"], \
                                      "image" : [".ani", ".bmp", ".cal", ".fax", ".gif", ".img", \
                                                ".jbg", ".jpe", ".jpeg", ".jpg", ".mac", ".pbm", \
                                                ".pcd", ".pcx", ".pct", ".pgm", ".png", ".ppm", \
                                                ".psd", ".ras", ".tga", ".tiff", ".wmf"], \
                                      "pdf" : [".pdf"], \
                                      "text_files" : [".dot", ".txt", ".docx", ".dotx", ".epub", \
                                      ".odt", ".ott", ".odm", ".md"]}


    def is_concerned(self, channel_id: str):
        """Returns true if the channel_id is concerned by at least one conversation"""
        for com in self.communications:
            for channel in self.communications[com].channels:
                if channel == channel_id:
                    return True
        return False


    @commands.command()
    @checks.is_owner()
    async def add_conv(self, conv_name: str, *channels):
        """Adds a conversation
        Parameters:
            conv_name: The name you want to use for the conversation (no spaces).
            *channels: The list of the channels IDs for the conversation, separated by spaces.

        Example: [p]add_conv myFirstConv 347571375466086401 346323687554809857 345548753366810625"""

        if conv_name not in self.communications:

            for com in channels:
                channel = discord.utils.find(lambda x, c=com: x.id == c, \
                                            self.bot.get_all_channels())
                if channel:

                    perms = channel.permissions_for(discord.utils.find( \
                            lambda m: m.id == self.bot.user.id, channel.server.members))

                    if not perms.read_messages:
                        await self.bot.say(":warning: Can't read messages in #" + \
                                channel.name + ", in server " + channel.server.name)

                    if not perms.send_messages:
                        await self.bot.say(":warning: Can't send messages in #" + \
                                channel.name + ", in server " + channel.server.name)

                else:
                    await self.bot.say(":warning: I don't have access to the channel with " \
                            + com + " as ID! Please ensure the channel exists and that the bot " \
                            + "is in the server and have `Read message` + `Send messages` " \
                            + "permissions in this channel!")

            self.communications[conv_name] = Conversation([x for x in channels])
            self.save()
            await self.bot.say("Conversation added! :ok_hand:")

        else:
            await self.bot.say("A conversation with this name already exists!" \
                    + " Please choose another name, or edit the existing conversation!")


    @commands.command()
    @checks.is_owner()
    async def rem_conv(self, conv_name: str):
        """Removes a conversation
        Parameters:
            conv_name: The name of the conversation you want to remove.

        Example: [p]rem_conv myFirstConv"""
        if conv_name in self.communications:
            del self.communications[conv_name]
            self.save()
            await self.bot.say("The conversation `" + conv_name + "` has been removed. :ok_hand:")
        else:
            await self.bot.say("There's no conversation with such name. " \
                    + "To get the list of the conversation, type `[p]list_conv`.")


    @commands.command()
    @checks.is_owner()
    async def list_conv(self):
        """Lists all the conversations"""
        if self.communications: #length different from 0
            msg = "```Markdown\nList of the conversations\n========================\n\n"
            i = 1
            for com in self.communications:
                msg += "[" + str(i) + "](" + com + ")\n"
                i += 1
            msg += "```\nIf you want more details about a specific conversations, " \
                    + "type `[p]get_conv_details conv_name`."
            await self.bot.say(msg)
        else:
            await self.bot.say("There's no conversations! :grimacing:")

    @commands.command()
    @checks.is_owner()
    async def get_conv_details(self, conv_name: str):
        """Shows all the details about a conversation
        Parameters:
            conv_name: The name of the conversation you want the details.

        Example: [p]get_conv_details myFirstConv"""
        #pylint: disable=too-many-branches

        if conv_name in self.communications:
            msg = "Details for `" + conv_name + "`:\n\nChannels:\n---------------\n\n"
            i = 1
            for com in self.communications[conv_name].channels:
                msg += "\t" + str(i) + ") "
                channel = discord.utils.find(lambda x, c=com: x.id == c, \
                                            self.bot.get_all_channels())
                if channel:
                    msg += channel.name + " (in server " + channel.server.name + ")\n"

                    perms = channel.permissions_for(discord.utils.find( \
                            lambda m: m.id == self.bot.user.id, channel.server.members))

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
                    msg += "`UNKNOWN CHANNEL` (" + com + ") :x:"

                msg += "\n"
                i += 1
            msgs = msg.split("\n")
            final_msgs = [[msgs[0] + "\n", len(msgs[0])]]
            tracker = 0
            for cut_msg in msgs:
                msg_length = len(cut_msg)
                if msg_length + final_msgs[tracker][1] <= 1997:
                    final_msgs[tracker][0] += cut_msg + "\n"
                    final_msgs[tracker][1] += msg_length + 2
                else:
                    final_msgs.append([cut_msg + "\n", len(cut_msg)])
                    tracker += 1
            for msg_to_send in final_msgs:
                await self.bot.say(msg_to_send[0])
        else:
            await self.bot.say("There's no conversation with such name. " \
                    + "To get the list of the conversation, type `[p]list_conv`.")


    @commands.command()
    @checks.is_owner()
    async def add_channels_conv(self, conv_name: str, *channels):
        """Adds channels to a conversation
        Parameters:
            conv_name: The name of the conversation you want to add channels to.
            channels: The list of the channels IDs you want to add, separated by spaces.

        Example:    [p]add_channels_conv myFirstConv 347571375466086401 346323687554809857
                    [p]add_channels_conv myFirstConv 347571375466086401"""
        if conv_name in self.communications:
            msg = ""
            for chan in channels:
                if chan not in self.communications[conv_name].channels:
                    channel = discord.utils.find(lambda x, c=chan: x.id == c, \
                                                self.bot.get_all_channels())
                    if channel:
                        perms = channel.permissions_for(discord.utils.find( \
                                lambda m: m.id == self.bot.user.id, channel.server.members))
                        if not perms.read_messages:
                            msg += ":warning: Cant't read messages in " + channel.name + \
                                    " (server: " + channel.server.name + ").\n"
                        if not perms.send_messages:
                            msg += ":warning: Cant't send messages in " + channel.name + \
                                    " (server: " + channel.server.name + ").\n"
                    else:
                        msg += ":warning: I don't have access to the channel with " + chan + \
                                " as ID! Please ensure the channel exists and that the bot is " + \
                                "in the server and have \"Read message\" + \"Send messages\"" + \
                                "permissions in this channel!\n"
                    self.communications[conv_name].channels.append(chan)
                else:
                    msg += chan + " is already registered in this conversation.\n"
            self.save()
            msg += "The channels have been added to the conversation `" + conv_name + "`."
            await self.bot.say(msg)
        else:
            await self.bot.say("There's no conversation with such name. " + \
                    "To get the list of the conversation, type `[p]list_conv`.")

    @commands.command()
    @checks.is_owner()
    async def rem_channels_conv(self, conv_name: str, *channels):
        """Removes channels from a conversation
        Parameters:
            conv_name: The name of the conversation you want to remove channels from.
            channels: The list of the channels IDs you want to remove, separated by spaces.

        Example:    [p]rem_channels_conv myFirstConv 347571375466086401 346323687554809857
                    [p]rem_channels_conv myFirstConv 347571375466086401"""
        if conv_name in self.communications:
            msg = ""
            for chan in channels:
                if chan in self.communications[conv_name].channels:
                    channel = discord.utils.find(lambda x, c=chan: x.id == c, \
                                                self.bot.get_all_channels())
                    if channel:
                        msg += "Channel #" + channel.name + " (server: " + \
                                channel.server.name + ") has been removed from the conversation.\n"
                    else:
                        msg += "Channel with " + chan + \
                                " as ID has been removed from the conversation.\n"
                    self.communications[conv_name].channels.remove(chan)
                else:
                    msg += "The re's no channel with " + chan + " as ID in this conversation.\n"
            self.save()
            msg += "\nDone! :ok_hand:"
            await self.bot.say(msg)
        else:
            await self.bot.say("There's no conversation with such name. " + \
                    "To get the list of the conversation, type `[p]list_conv`.")


    @commands.command()
    @checks.is_owner()
    async def change_conv_name(self, conv_name: str, new_conv_name: str):
        """Changes the name of a conversation
        Parameters:
            conv_name: The current name of the conversation you want to change the name.
            new_conv_name: The new name for the conversation.

        Example: [p]change_conv_name myFirstConv mySecondConv"""
        if conv_name in self.communications:
            if new_conv_name not in self.communications:
                self.communications[new_conv_name] = self.communications[conv_name]
                del self.communications[conv_name]
                self.save()
                await self.bot.say("Done! :ok_hand:")
            else:
                await self.bot.say("There's already a conversation called `" + \
                                new_conv_name + "`. Please choose another name!")
        else:
            await self.bot.say("There's no conversation with such name. " + \
                    "To get the list of the conversation, type `[p]list_conv`.")


    async def check_communications(self, msg):
        """Checks for messages posts"""
        # pylint: disable=too-many-statements
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-nested-blocks
        if msg.author.id != self.bot.user.id and msg.author.id not in self.bot.blacklist:
            if self.is_concerned(msg.channel.id):

                embed_msg = discord.Embed(type="rich", description=msg.content, \
                                            colour=msg.author.colour)

                embed_msg.set_footer(text="In #" + msg.channel.name + " (server: " + \
                                    msg.server.name + ")", icon_url=msg.server.icon_url)
                embed_msg.set_author(name=msg.author.name + "#" + msg.author.discriminator + \
                                    " (" + msg.author.id + ")", \
                                    url=msg.author.avatar_url, icon_url=msg.author.avatar_url)

                if msg.attachments: #length different from 0
                    i = 1
                    image = False
                    for att in msg.attachments:
                        emote = None
                        extension = att["filename"][att["filename"].rfind("."):]
                        if extension in self.attachments_extensions["image"] and not image:
                            image = True
                            embed_msg.set_image(url=att["url"])
                        else:
                            for ext in self.attachments_extensions:
                                if extension in self.attachments_extensions[ext]:
                                    emote = self.attachments_emojis[ext]
                                    break
                            if not emote:
                                emote = self.attachments_emojis["others"]
                            embed_msg.add_field(name="Attachment #" + str(i), value=emote + " [" + \
                                            att["filename"] + "](" + att["url"] + ")", inline=False)
                            i += 1

                for com in self.communications:
                    if msg.channel.id in self.communications[com].channels:
                        for channel in self.communications[com].channels:
                            if channel != msg.channel.id:

                                channel_to_send = discord.utils.find(lambda c, chan=channel: \
                                                    c.id == chan, self.bot.get_all_channels())
                                if channel_to_send:
                                    try:
                                        message_to_store = await self.bot.send_message( \
                                                            channel_to_send, embed=embed_msg)
                                        if len(self.communications[com].messages) == 20:
                                            del self.communications[com].messages[0]
                                            self.communications[com].messages[len(self.communications[com].messages) - 1]["messages"].append([message_to_store, embed_msg]) # pylint: disable=line-too-long
                                        elif not self.communications[com].messages: #length equals 0
                                            self.communications[com].messages.append({"id": msg.id, "embed": embed_msg, "messages": [], "reactions": {}}) # pylint: disable=line-too-long
                                            self.communications[com].messages[len(self.communications[com].messages) - 1]["messages"].append(message_to_store) # pylint: disable=line-too-long
                                        elif self.communications[com].messages[len(self.communications[com].messages) - 1]["id"] == msg.id: # pylint: disable=line-too-long
                                            self.communications[com].messages[len(self.communications[com].messages) - 1]["messages"].append(message_to_store) # pylint: disable=line-too-long
                                        else:
                                            self.communications[com].messages.append({"id": msg.id, "embed": embed_msg, "messages": [], "reactions": {}}) # pylint: disable=line-too-long
                                            self.communications[com].messages[len(self.communications[com].messages) - 1]["messages"].append(message_to_store) # pylint: disable=line-too-long
                                    except discord.Forbidden:
                                        print("Can't send messages to #" + channel_to_send.name + " (server: " + channel_to_send.server.name + ")") # pylint: disable=line-too-long
                                    except discord.NotFound:
                                        print("I just lost access to #" + channel_to_send.name + " (server: " + channel_to_send.server.name + ")") # pylint: disable=line-too-long
                                    except discord.HTTPException:
                                        pass
                                    except discord.InvalidArgument:
                                        pass


    async def check_channels_deletes(self, channel):
        """Checks for channels deletions"""
        owner = discord.utils.find(lambda u: u.id == self.owner_id, self.bot.get_all_members())
        if owner:
            for conv in self.communications:
                if channel.id in self.communications[conv].channels:
                    await self.bot.send_message(owner, ":warning: The channel \"" + channel.name + \
                        "\" in the server \"" + channel.server.name + "\" has been deleted.\n" + \
                        ":warning: The communication `" + conv + "` is affected by this change.\n" \
                        + "You can remove this channel from this communication using " + \
                        "`rem_channel_conv " + conv + " " + channel.id + "`!")
        else:
            print("The owner has no servers in common with the bot!")


    async def check_channels_updates(self, before, after):
        """Checks for channels updates"""
        #pylint: disable=unused-argument
        for conv in self.communications:
            if after.id in self.communications[conv].channels:
                perms = after.permissions_for(discord.utils.find( \
                        lambda m: m.id == self.bot.user.id, after.server.members))
                owner = discord.utils.find(lambda u: u.id == self.owner_id, \
                                            self.bot.get_all_members())
                if owner:
                    if not perms.read_messages:
                        await self.bot.send_message(owner, ":warning: The channel \"" + \
                                after.name + "\" in the server \"" + after.server.name + \
                                "\" has been updated.\nI can't read messages there anymore!\n" \
                                + "The communication `" + conv + "` is affected by this change.")

                    if not perms.send_messages:
                        await self.bot.send_message(owner, ":warning: The channel \"" + after.name \
                        + "\" in the server \"" + after.server.name + "\" has been updated.\n" + \
                        "I can't send messages there!\nThe communication `" + conv + \
                        "` is affected by this change.")
                else:
                    print("The owner has no servers in common with the bot!")


    async def check_roles_changes(self, before, after):
        """Checks for roles changes"""
        #pylint: disable=unused-argument
        for conv in self.communications:
            for chan in self.communications[conv].channels:
                channel = discord.utils.find(lambda x, c=chan: x.id == c, after.server.channels)
                if channel:
                    perms = channel.permissions_for(discord.utils.find( \
                            lambda m: m.id == self.bot.user.id, after.server.members))
                    owner = discord.utils.find(lambda u: u.id == self.owner_id, \
                                                self.bot.get_all_members())
                    if owner:
                        if not perms.read_messages:
                            await self.bot.send_message(owner, ":warning: My permissions in the " \
                            + "server \"" + after.server.name + "\" have been updated.\nI can't" \
                            + " read messages in the channel \"" + channel.name + "\" anymore!\n" \
                            + "The communication `" + conv + "` is affected by this change.")

                        if not perms.send_messages:
                            await self.bot.send_message(owner, ":warning: My permissions in the " \
                            + "server \"" + after.server.name + "\" have been updated.\nI can't " \
                            + "send messages in the channel \"" + channel.name + "\"!\n" + \
                            "The communication `" + conv + "` is affected by this change.")
                    else:
                        print("The owner has no servers in common with the bot!")


    async def check_server_deletes(self, server):
        """Checks for servers deletions"""
        for conv in self.communications:
            for chan in self.communications[conv].channels:
                channel = discord.utils.find(lambda x, c=chan: x.id == c, server.channels)
                if channel:
                    owner = discord.utils.find(lambda o: o.id == self.owner_id, \
                                                self.bot.get_all_members())
                    if owner:
                        await self.bot.send_message(owner, ":warning: I'm not in the server \"" + \
                            server.name + "\" anymore. I can't access to the channel " + \
                            channel.name + " anymore!\nThe communication `" + conv + \
                            "` is affected by this change.")
                    else:
                        print("The owner has no servers in common with the bot!")


    async def check_roles_deletes(self, role):
        """Checks for roles deletions"""
        for conv in self.communications:
            for chan in self.communications[conv].channels:
                channel = discord.utils.find(lambda x, c=chan: x.id == c, role.server.channels)
                if channel:
                    perms = channel.permissions_for(discord.utils.find( \
                            lambda m: m.id == self.bot.user.id, role.server.members))
                    owner = discord.utils.find(lambda u: u.id == self.owner_id, \
                                                self.bot.get_all_members())
                    if owner:
                        if not perms.read_messages:
                            await self.bot.send_message(owner, ":warning: My permissions in " + \
                            "the server \"" + role.server.name + "\" have been updated.\n" + \
                            "I can't read messages in the channel \"" + channel.name + "\" a" + \
                            "nymore!\nThe communication `" + conv + "` is affected by this change.")

                        if not perms.send_messages:
                            await self.bot.send_message(owner, ":warning: My permissions in the " +\
                            "server \"" + role.server.name + "\" have been updated.\n" + \
                            "I can't send messages in the channel \"" + channel.name + "\"!\n" + \
                            "The communication `" + conv + "` is affected by this change.")
                    else:
                        print("The owner has no servers in common with the bot!")


    async def check_roles_updates(self, before, after):
        """Check for roles updates"""
        #pylint: disable=unused-argument
        for conv in self.communications:
            for chan in self.communications[conv].channels:
                channel = discord.utils.find(lambda x, c=chan: x.id == c, after.server.channels)
                if channel:
                    perms = channel.permissions_for(discord.utils.find( \
                            lambda m: m.id == self.bot.user.id, after.server.members))
                    owner = discord.utils.find(lambda u: u.id == self.owner_id, \
                                                self.bot.get_all_members())
                    if owner:
                        if not perms.read_messages:
                            await self.bot.send_message(owner, ":warning: My permissions in the" \
                            + "server \"" + after.server.name + "\" have been updated.\nI can't " \
                            + "read messages in the channel \"" + channel.name + "\" anymore!\n" + \
                            "The communication `" + conv + "` is affected by this change.")

                        if not perms.send_messages:
                            await self.bot.send_message(owner, ":warning: My permissions in the " \
                            + "server \"" + after.server.name + "\" have been updated.\nI can't " \
                            + "send messages in the channel \"" + channel.name + "\"!\n" + \
                            "The communication `" + conv + "` is affected by this change.")
                    else:
                        print("The owner has no servers in common with the bot!")


    async def check_messages_edits(self, before, after):
        """Check for messages edits"""
        #pylint: disable=unused-argument
        #pylint: disable=too-many-nested-blocks
        if after.author.id not in self.bot.blacklist:
            for conv in self.communications:
                for msg in self.communications[conv].messages:
                    if after.id == msg["id"]:
                        msg["embed"].description = after.content
                        for message in msg["messages"]:
                            try:
                                await self.bot.edit_message(message, embed=msg["embed"])
                            except discord.HTTPException:
                                pass


    async def check_messages_deletes(self, msg):
        """Checks for messages deletions"""
        #pylint: disable=too-many-nested-blocks
        if msg.author.id not in self.bot.blacklist:
            for conv in self.communications:
                for message in self.communications[conv].messages:
                    if msg.id == message["id"]:
                        for message_sent in message["messages"]:
                            try:
                                await self.bot.delete_message(message_sent)
                            except discord.Forbidden:
                                print("What?!!! o_O")
                            except discord.HTTPException:
                                pass


    async def check_reactions_add(self, reaction, user):
        """Check for reactions additions"""
        #pylint: disable=unused-argument
        #pylint: disable=too-many-nested-blocks
        #pylint: disable=too-many-branches
        if user.id not in self.bot.blacklist:
            for com in self.communications:
                for msg in self.communications[com].messages:
                    if reaction.message.id == msg["id"]:
                        emoji_id = ""
                        emoji_output = ""
                        if isinstance(reaction.emoji, str):
                            emoji_id = reaction.emoji
                            emoji_output = emoji_id
                        else:
                            emoji_id = reaction.emoji.id
                            emoji_output = ":" + reaction.emoji.name + ":"

                        if emoji_id not in msg["reactions"]:
                            msg["reactions"][emoji_id] = 1
                        else:
                            msg["reactions"][emoji_id] += 1

                        index = -1
                        for i in range(0, len(msg["embed"].fields)):
                            if msg["embed"].fields[i].name == "Reactions":
                                index = i
                                break

                        old_value = ""
                        if index != -1:
                            old_value = msg["embed"].fields[index].value

                        new_value = ""
                        if msg["reactions"][emoji_id] == 1:
                            new_value = old_value + emoji_output + " - 1\n"
                        else:
                            new_value = ""
                            for line in msg["embed"].fields[index].value.splitlines():
                                if line.startswith(emoji_output):
                                    line_index = line.find(" - ")
                                    new_value += line[:line_index + 3] + \
                                                str(int(line[line_index + 3:]) + 1) + "\n"
                                else:
                                    new_value += line + "\n"
                        if index == -1:
                            msg["embed"].add_field(name="Reactions", inline=False, value=new_value)
                        else:
                            msg["embed"].remove_field(index)
                            msg["embed"].add_field(name="Reactions", inline=False, value=new_value)

                        for message_sent in msg["messages"]:
                            try:
                                await self.bot.edit_message(message_sent, embed=msg["embed"])
                            except discord.HTTPException:
                                pass

    async def check_reactions_remove(self, reaction, user):
        """Check for reactions deletions"""
        #pylint: disable=unused-argument
        #pylint: disable=too-many-nested-blocks
        #pylint: disable=too-many-branches
        if user.id not in self.bot.blacklist:
            for com in self.communications:
                for msg in self.communications[com].messages:
                    if reaction.message.id == msg["id"]:
                        emoji_id = ""
                        emoji_output = ""
                        if isinstance(reaction.emoji, str):
                            emoji_id = reaction.emoji
                            emoji_output = emoji_id
                        else:
                            emoji_id = reaction.emoji.id
                            emoji_output = ":" + reaction.emoji.name + ":"

                        msg["reactions"][emoji_id] -= 1
                        if msg["reactions"][emoji_id] == 0:
                            del msg["reactions"][emoji_id]

                        for i in range(0, len(msg["embed"].fields)):
                            if msg["embed"].fields[i].name == "Reactions":
                                index = i
                                break

                        new_value = ""
                        for line in msg["embed"].fields[index].value.splitlines():
                            if line.startswith(emoji_output):
                                if emoji_id in msg["reactions"]:
                                    line_index = line.find(" - ")
                                    new_value += line[:line_index + 3] + \
                                                    str(int(line[line_index + 3:]) - 1) + "\n"
                            else:
                                new_value += line + "\n"

                        msg["embed"].remove_field(index)
                        if msg["reactions"]:
                            msg["embed"].add_field(name="Reactions", inline=False, value=new_value)

                        for message_sent in msg["messages"]:
                            try:
                                await self.bot.edit_message(message_sent, embed=msg["embed"])
                            except discord.HTTPException:
                                pass


    async def check_reactions_clear(self, message, reactions):
        """Checks for reactions clears"""
        #pylint: disable=unused-argument
        #pylint: disable=too-many-nested-blocks
        if message.author.id not in self.bot.blacklist:
            for com in self.communications:
                for msg in self.communications[com].messages:
                    if msg["id"] == message.id:
                        msg["reactions"] = {}

                        index = -1
                        for i in range(0, len(msg["embed"].fields)):
                            if msg["embed"].fields[i].name == "Reactions":
                                index = i
                                break

                        if index != -1:
                            msg["embed"].remove_field(index)

                        for message_sent in msg["messages"]:
                            try:
                                await self.bot.edit_message(message_sent, embed=msg["embed"])
                            except discord.HTTPException:
                                pass



def setup(bot):
    """Setup function"""
    mod = Communications(bot)
    bot.add_listener(mod.check_communications, "on_message")
    bot.add_listener(mod.check_channels_deletes, "on_channel_delete")
    bot.add_listener(mod.check_channels_updates, "on_channel_update")
    bot.add_listener(mod.check_roles_changes, "on_member_update")
    bot.add_listener(mod.check_server_deletes, "on_server_remove")
    bot.add_listener(mod.check_roles_deletes, "on_server_role_delete")
    bot.add_listener(mod.check_roles_updates, "on_server_role_update")
    bot.add_listener(mod.check_messages_edits, "on_message_edit")
    bot.add_listener(mod.check_messages_deletes, "on_message_delete")
    bot.add_listener(mod.check_reactions_add, "on_reaction_add")
    bot.add_listener(mod.check_reactions_remove, "on_reaction_remove")
    bot.add_listener(mod.check_reactions_clear, "on_reaction_clear")
    bot.add_cog(mod)
