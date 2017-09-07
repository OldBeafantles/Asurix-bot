"""Admin module"""
import os
import math
from datetime import datetime
import copy
import discord
from discord.ext import commands
from modules.utils import checks
from modules.utils import utils


def is_owner_or_moderator(ctx):
    """Returns true if the author is the bot's owner or a moderator on the server"""
    return ctx.message.author.id == ctx.bot.owner_id \
        or (ctx.message.server.id in ctx.bot.cogs["Admin"].moderators \
            and ctx.message.author.id in ctx.bot.cogs["Admin"].moderators[ctx.message.server.id])

COLORS = { \
            "Unban": 255 * math.pow(16, 2), \
            "Warning": 250 * math.pow(16, 4) + 219 * math.pow(16, 2) + 24, \
            "Kick": 243 * math.pow(16, 4) + 111 * math.pow(16, 2) + 40, \
            "Ban": 255 * math.pow(16, 4), \
            "b1nzy ban": 1 \
         }


class Log:
    """A class representing a log element"""

    id_counter = 1

    def __init__(self, log_type: str, member_id: str, \
                responsible_id: str, reason: str, date: str):
        """Init function"""
        #pylint: disable=too-many-arguments
        self.type = log_type
        self.user_id = member_id
        self.responsible_id = responsible_id
        self.reason = reason
        self.date = date
        self.log_id = Log.id_counter
        Log.id_counter += 1

    def get_save(self):
        """Returns a dict representing a log element"""
        data = {}
        data["type"] = self.type
        data["responsible"] = self.responsible_id
        data["reason"] = self.reason
        data["date"] = self.date
        data["id"] = self.log_id
        return data


    def get_embed(self, bot):
        """Returns an embed corresponding to the log"""
        embed = discord.Embed()
        user = discord.utils.find(lambda u: u.id == self.user_id, \
                                    bot.get_all_members())
        if user:
            embed.title = user.name + "#" + user.discriminator + " (" + user.id + ")"
            embed.set_thumbnail(url=user.avatar_url)
        else:
            embed.title = "Unknown member (" + self.user_id + ")"
        responsible = discord.utils.find(lambda u: u.id == self.responsible_id, \
                                    bot.get_all_members())
        if responsible:
            embed.add_field(name="Responsible", \
                        value=responsible.name + "#" + responsible.discriminator + \
                        " (" + responsible.id + ")", inline=False)
        else:
            embed.add_field(name="Responsible", \
                        value="Uknown responsible (" + self.responsible_id + ")", inline=False)

        embed.timestamp = datetime.strptime(self.date, "%d/%m/%Y %H:%M:%S")
        embed.colour = discord.Colour(value=COLORS[self.type])
        embed.set_author(name="Case #" + str(self.log_id))
        embed.add_field(name="Reason", value=self.reason, inline=False)
        return embed


class Admin:
    """Admin module"""
    #pylint: disable=too-many-public-methods

    def load_moderators(self):
        """Loads the moderators"""
        if not os.path.exists(self.moderators_file_path):

            if not os.path.isdir("data/admin"):
                os.makedirs("data/admin")

            utils.save_json(self.moderators, self.moderators_file_path)
        else:
            self.moderators = utils.load_json(self.moderators_file_path)

    def save_moderators(self):
        """Saves the moderators"""
        utils.save_json(self.moderators, self.moderators_file_path)


    def load_servers_config(self):
        """Loads the configuration"""
        #pylint: disable=too-many-nested-blocks
        if not os.path.exists(self.servers_config_file_path):

            if not os.path.isdir("data/admin"):
                os.makedirs("data/admin")

            self.servers_config["id counter"] = 1
            self.servers_config["servers"] = {}
            Log.id_counter = 1
            utils.save_json(self.servers_config, self.servers_config_file_path)
        else:
            data = utils.load_json(self.servers_config_file_path)
            for server in data["servers"]:
                if "log channel" in data["servers"][server]:
                    data["servers"][server]["log channel"] = discord.utils.find(lambda c, s=server:\
                            c.id == data["servers"][s]["log channel"], self.bot.get_all_channels())
                if "logs" in data["servers"][server]:
                    logs = {}
                    known_admins = {}
                    for user_id in data["servers"][server]["logs"]:
                        member = discord.utils.find(lambda m, u=user_id: m.id == u, \
                                                    self.bot.get_all_members())
                        logs[user_id] = []
                        for log in data["servers"][server]["logs"][user_id]:
                            if log["responsible"] not in known_admins:
                                responsible = discord.utils.find(lambda r, l=log: \
                                        r.id == l["responsible"], self.bot.get_all_members())
                                known_admins[log["responsible"]] = responsible
                            else:
                                responsible = known_admins[log["responsible"]]
                            logs[user_id].append(Log(log_type=log["type"], member_id=member.id, \
                                            responsible_id=responsible.id, reason=log["reason"], \
                                            date=log["date"]))
                    data["servers"][server]["logs"] = logs
            Log.id_counter = data["id counter"]
            self.servers_config = data


    def save_servers_config(self):
        """Saves the configuration"""
        self.servers_config["id counter"] = Log.id_counter
        data = copy.deepcopy(self.servers_config)
        for server in data["servers"]:
            if "log channel" in data["servers"][server]:
                data["servers"][server]["log channel"] = data["servers"][server]["log channel"].id
            if "logs" in data["servers"][server]:
                logs = {}
                for user_id in data["servers"][server]["logs"]:
                    logs[user_id] = []
                    for log in data["servers"][server]["logs"][user_id]:
                        logs[user_id].append(log.get_save())
                data["servers"][server]["logs"] = logs
        utils.save_json(data, self.servers_config_file_path)


    def load_b1nzy_banlist(self):
        """Loads the b1nzy banlist"""
        if not os.path.exists(self.b1nzy_banlist_path):

            if not os.path.isdir("data/admin"):
                os.makedirs("data/admin")

            utils.save_json(self.b1nzy_banlist, self.b1nzy_banlist_path)
        else:
            self.b1nzy_banlist = utils.load_json(self.b1nzy_banlist_path)


    def save_b1nzy_banlist(self):
        """Saves the b1nzy banlist"""
        utils.save_json(self.b1nzy_banlist, self.b1nzy_banlist_path)


    def __init__(self, bot):
        """Init function"""
        self.bot = bot
        self.servers_config = {}
        self.servers_config_file_path = "data/admin/servers_config.json"
        self.load_servers_config()
        self.moderators = {}
        self.moderators_file_path = "data/admin/moderators.json"
        self.load_moderators()
        self.b1nzy_banlist = {}
        self.b1nzy_banlist_path = "data/admin/b1nzy_banlist.json"
        self.load_b1nzy_banlist()


    async def send_log(self, server: discord.Server, log: Log):
        """Sends a embed corresponding to the log in the log channel of the server"""
        if server.id in self.servers_config["servers"]:
            if "log channel" in self.servers_config["servers"][server.id]:
                embed = log.get_embed(self.bot)
                channel = self.servers_config["servers"][server.id]["log channel"]
                try:
                    await self.bot.send_message(destination=channel, embed=embed)
                except discord.Forbidden:
                    await self.bot.send_message(destination=server.owner, content=\
                        "I'm not allowed to send embeds in the log channel (#" + \
                        channel.name + "). Please change my permissions.")
                except discord.NotFound:
                    await self.bot.send_message(destination=server.owner, content=\
                        "I'm not allowed to send embeds in the log channel because " + \
                        "it doesn't exists anymore. Please set another log channel " + \
                        "using the `[p]set_log_channel` command.")
                except discord.HTTPException:
                    pass
                except discord.InvalidArgument:
                    pass


    @commands.command()
    @checks.is_owner()
    async def add_blacklist(self, user: discord.Member):
        """Adds an user to the bot's blacklist
        Parameters:
            user: The user you want to add to the bot's blacklist.

        Example: [p]add_blacklist @AVeryMeanUser"""
        if user.id not in self.bot.blacklist:
            self.bot.blacklist.append(user.id)
            utils.save_json(self.bot.blacklist, self.bot.blacklist_file_path)
            await self.bot.say("Done.")
        else:
            await self.bot.say(user.name + "#" + user.discriminator + " (" + \
                user.id + ") is already blacklisted.")


    @commands.command()
    @checks.is_owner()
    async def add_blacklist_id(self, user_id: str):
        """Adds an user to the bot's blacklist using his ID
        Parameters:
            user_id: The ID of the user you want to add to the bot's blacklist.

        Example: [p]add_blacklist_id 346654353341546499"""
        if user_id not in self.bot.blacklist:
            self.bot.blacklist.append(user_id)
            utils.save_json(self.bot.blacklist, self.bot.blacklist_file_path)
            await self.bot.say("Done.")
        else:
            await self.bot.say("This ID is already in the blacklist.")


    @commands.command()
    @checks.is_owner()
    async def rem_blacklist(self, user: discord.Member):
        """Removes an user from the bot's blacklist
        Parameters:
            user: The user you want to remove from the bot's blacklist.

        Example: [p]rem_blacklist @AGoodGuyUnfairlyBlacklisted"""
        if user.id in self.bot.blacklist:
            self.bot.blacklist.remove(user.id)
            utils.save_json(self.bot.blacklist, self.bot.blacklist_file_path)
            await self.bot.say("Done.")
        else:
            await self.bot.say("This user wasn't even blacklisted.")


    @commands.command()
    @checks.is_owner()
    async def rem_blacklist_id(self, user_id: str):
        """Removes an user from the bot's blacklist using his ID
        Parameters:
            user_id: The ID of the user you want to to remove from the bot's blacklist.

        Example: [p]rem_blacklist @AGoodGuyUnfairlyBlacklisted"""
        if user_id in self.bot.blacklist:
            self.bot.blacklist.remove(user_id)
            utils.save_json(self.bot.blacklist, self.bot.blacklist_file_path)
            await self.bot.say("Done.")
        else:
            await self.bot.say("This ID wasn't even in the blacklist.")

    @commands.command(pass_context=True)
    @checks.is_owner_or_server_owner()
    async def add_moderator(self, ctx, member: discord.Member):
        """Adds a moderator for the server
        Parameters:
            member: The member that will become a moderator.

        Example: [p]add_moderator @Beafantles"""
        if ctx.message.server.id not in self.moderators:
            self.moderators[ctx.message.server.id] = [member.id]
        else:
            if member.id not in self.moderators[ctx.message.server.id]:
                self.moderators[ctx.message.server.id].append(member.id)
            else:
                await self.bot.say(member.name + "#" + member.discriminator + \
                        " is already a moderator on this server.")
                return
        self.save_moderators()
        await self.bot.say("Done.")


    @commands.command(pass_context=True)
    @checks.is_owner_or_server_owner()
    async def add_moderator_id(self, ctx, member_id: str):
        """Adds a moderator for the server using his ID
        Parameters:
            member_id: The ID of the member that will become a moderator.

        Example: [p]add_moderator_id 151661401411289088"""
        member = discord.utils.find(lambda m: m.id == member_id, \
                                    ctx.message.server.members)
        if member:
            if ctx.message.server.id not in self.moderators:
                self.moderators[ctx.message.server.id] = [member.id]
            else:
                if member.id not in self.moderators[ctx.message.server.id]:
                    self.moderators[ctx.message.server.id].append(member.id)
                else:
                    await self.bot.say(member.name + "#" + member.discriminator + \
                            " is already a moderator on this server.")
                    return
            self.save_moderators()
            await self.bot.say("Done.")
        else:
            await self.bot.say("There's no member with such ID on this server.")


    @commands.command(pass_context=True)
    @checks.is_owner_or_server_owner()
    async def rem_moderator(self, ctx, moderator: discord.Member):
        """Removes a moderator
        Parameters:
            moderator: The moderator you want to revoke.

        Example: [p]rem_moderator @Kazutsuki"""
        if ctx.message.server.id in self.moderators:
            if moderator.id in self.moderators[ctx.message.server.id]:
                self.moderators[ctx.message.server.id].remove(moderator.id)
                if not self.moderators[ctx.message.server.id]:
                    del self.moderators[ctx.message.server.id]
                self.save_moderators()
                await self.bot.say("Done.")
            else:
                await self.bot.say(moderator.name + "#" + moderator.discriminator + \
                        " wasn't even a moderator on this server.")
        else:
            await self.bot.say("There's no moderators on this server.")


    @commands.command(pass_context=True)
    @checks.is_owner_or_server_owner()
    async def rem_moderator_id(self, ctx, moderator_id: str):
        """Removes a moderator
        Parameters:
            moderator_id: The ID of the moderator you want to revoke.

        Example: [p]rem_moderator_id 118473388262948869"""
        moderator = discord.utils.find(lambda m: m.id == moderator_id, \
                    ctx.message.server.members)
        if moderator:
            if ctx.message.server.id in self.moderators:
                if moderator.id in self.moderators[ctx.message.server.id]:
                    self.moderators[ctx.message.server.id].remove(moderator.id)
                    if not self.moderators[ctx.message.server.id]:
                        del self.moderators[ctx.message.server.id]
                    self.save_moderators()
                    await self.bot.say("Done.")
                else:
                    await self.bot.say(moderator.name + "#" + moderator.discriminator + \
                            " wasn't even a moderator on this server.")
            else:
                await self.bot.say("There's no moderators on this server.")
        else:
            await self.bot.say("There's no member with such ID on this server.")


    @commands.command(pass_context=True)
    @checks.is_owner_or_server_owner()
    async def list_moderators(self, ctx):
        """Lists all the moderators on this server"""
        if ctx.message.server.id in self.moderators:
            msg = "```Markdown\nModerators on this server\n========================\n\n"
            has_unknown = False
            i = 1
            for mod_id in self.moderators[ctx.message.server.id]:
                msg += str(i) + ". "
                moderator = discord.utils.find(lambda m, mod=mod_id: m.id == mod, \
                            ctx.message.server.members)
                if moderator:
                    msg += moderator.name + "#" + moderator.discriminator +  " (" + \
                            moderator.id + ")"
                else:
                    msg += "Unknown moderator"
                    has_unknown = True
                msg += "\n"
                i += 1
            msg += "```"
            if has_unknown:
                msg += "`Unknown` means that this moderator isn't on this server anymore."
            await self.bot.say(msg)
        else:
            await self.bot.say("There's no moderators on this server.")


    @commands.command()
    @checks.is_owner()
    async def list_blacklist(self):
        """Lists all the blacklisted users"""
        if self.bot.blacklist:
            msg = "```Markdown\nList of blacklisted users:\n=================\n\n"
            i = 1
            has_unknown = False
            for user_id in self.bot.blacklist:
                user = discord.utils.find(lambda u, u_id=user_id: u.id == u_id, \
                                            self.bot.get_all_members())
                msg += str(i) + ". "
                if user:
                    msg += user.name + "#" + user.discriminator + " (" + user.id + ")\n"
                else:
                    has_unknown = True
                    msg += "UNKNOWN USER\n"
                i += 1
            msg += "```"
            if has_unknown:
                msg += "\n`UNKNOWN USER` means that this user hasn't any server in " + \
                        "common with the bot."
            await self.bot.say(msg)
        else:
            await self.bot.say("There is no blacklisted users.")


    @commands.command(pass_context=True)
    @checks.is_owner_or_server_owner()
    async def set_log_channel(self, ctx, channel: discord.Channel=None):
        """Set's log channel for warn / mute / kick / ban commands
        Parameters:
            channel: The channel you want to set for the logs.
                     Leaving this blank will remove the channel for logs.abs

        Example: [p]set_log_channel #logs-channel
                 [p]set_log_channel"""
        bot = discord.utils.find(lambda m: m.id == self.bot.user.id, \
                                ctx.message.server.members)
        if bot:
            if channel:
                permissions = channel.permissions_for(bot)
                if permissions.send_messages:
                    if ctx.message.server.id in self.servers_config["servers"]:
                        self.servers_config["servers"][ctx.message.server.id]["log channel"] = channel #pylint: disable=line-too-long
                    else:
                        self.servers_config["servers"][ctx.message.server.id] = {"log channel": channel} #pylint: disable=line-too-long
                    self.save_servers_config()
                    await self.bot.say("Done. :ok_hand:")
                else:
                    await self.bot.say("I'm not allowed to send messages there.\n" + \
                                        "(Missing permissions)")
            else:
                if ctx.message.server.id in self.servers_config["servers"]:
                    del self.servers_config["servers"][ctx.message.server.id]["log channel"]
                    self.save_servers_config()
                await self.bot.say("Done! :ok_hand:")


    @commands.command(pass_context=True)
    @checks.custom(is_owner_or_moderator)
    async def show_log_channel(self, ctx):
        """Shows the log channel of the server"""
        if ctx.message.server.id in self.servers_config["servers"] \
            and "log channel" in self.servers_config["servers"][ctx.message.server.id]:
            channel = self.servers_config["servers"][ctx.message.server.id]["log channel"]
            await self.bot.say("Log channel: <#" + channel.id + ">")
        else:
            await self.bot.say("There's no log channel set on this server.")


    @commands.command(pass_context=True)
    @checks.custom(is_owner_or_moderator)
    async def warn(self, ctx, member: discord.Member, *reason):
        """Warns a member
        Parameters:
            member: The member you want to warn.
            *reason: The reason of the warning.

        Example: [p]warn @BagGuy Rude words.
                 [p]warn @AnotherBadGuy"""
        reason = " ".join(reason)
        log = Log(log_type="Warning", member_id=member.id, \
                responsible_id=ctx.message.author.id, reason=reason, \
                date=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        if ctx.message.server.id not in self.servers_config["servers"]:
            self.servers_config["servers"][ctx.message.server.id] = {}
        if "logs" not in self.servers_config["servers"][ctx.message.server.id]:
            self.servers_config["servers"][ctx.message.server.id]["logs"] = {}
        if member.id in self.servers_config["servers"][ctx.message.server.id]["logs"]:
            self.servers_config["servers"][ctx.message.server.id]["logs"][member.id].append(log)
        else:
            self.servers_config["servers"][ctx.message.server.id]["logs"][member.id] = [log]
        self.save_servers_config()
        await self.send_log(server=ctx.message.server, log=log)
        await self.bot.say("Done.")

    @commands.command(pass_context=True)
    @checks.custom(is_owner_or_moderator)
    async def warn_id(self, ctx, member_id: str, *reason):
        """Warns a member
        Parameters:
            member_id: The ID of the member you want to warn.
            *reason: The reason of the warning.

        Example: [p]warn 346654353341546499 Rude words.
                 [p]warn 346654353341546499"""
        member = discord.utils.find(lambda m: m.id == member_id, \
                                ctx.message.server.members)
        if member:
            reason = " ".join(reason)
            log = Log(log_type="Warning", member_id=member.id, \
                    responsible_id=ctx.message.author.id, reason=reason, \
                    date=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            if not ctx.message.server.id in self.servers_config["servers"]:
                self.servers_config["servers"][ctx.message.server.id] = {}
            if not "logs" in self.servers_config["servers"][ctx.message.server.id]:
                self.servers_config["servers"][ctx.message.server.id]["logs"] = {}
            if member.id in self.servers_config["servers"][ctx.message.server.id]["logs"]:
                self.servers_config["servers"][ctx.message.server.id]["logs"][member.id].append(log)
            else:
                self.servers_config["servers"][ctx.message.server.id]["logs"][member.id] = [log]
            self.save_servers_config()
            await self.send_log(server=ctx.message.server, log=log)
            await self.bot.say("Done.")
        else:
            await self.bot.say("There's no member with such ID on this server.")


    @commands.command(pass_context=True)
    @checks.custom(is_owner_or_moderator)
    async def kick(self, ctx, member: discord.Member, *reason):
        """Kicks a member
        Parameters:
            member: The member you want to kick.
            *reason: The reason of the kick.

        Example: [p]kick @ABadGuy He was too rude.
                 [p]kick @AnotherBadGuy"""
        try:
            await self.bot.kick(member)
            reason = " ".join(reason)
            log = Log(log_type="Kick", member_id=member.id, responsible_id=ctx.message.author.id, \
                    reason=reason, date=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            if not ctx.message.server.id in self.servers_config["servers"]:
                self.servers_config["servers"][ctx.message.server.id] = {}
            if not "logs" in self.servers_config["servers"][ctx.message.server.id]:
                self.servers_config["servers"][ctx.message.server.id]["logs"] = {}
            if member.id in self.servers_config["servers"][ctx.message.server.id]["logs"]:
                self.servers_config["servers"][ctx.message.server.id]["logs"][member.id].append(log)
            else:
                self.servers_config["servers"][ctx.message.server.id]["logs"][member.id] = [log]
            self.save_servers_config()
            await self.send_log(server=ctx.message.server, log=log)
            await self.bot.say("Done.")
        except discord.Forbidden:
            await self.bot.say("I'm not allowed to do that.\n" + \
                                        "(Missing permissions)")


    @commands.command(pass_context=True)
    @checks.custom(is_owner_or_moderator)
    async def kick_id(self, ctx, member_id: str, *reason):
        """Kicks a member using his ID
        Parameters:
            member_id: The ID of member you want to kick.
            *reason: The reason of the kick.

        Example: [p]kick_id 346654353341546499 Bad guy.
                 [p]kick_id 346654353341546499"""
        try:
            member = discord.utils.find(lambda m: m.id == member_id, \
                                        ctx.message.server.members)
            if member:
                await self.bot.kick(member)
                reason = " ".join(reason)
                log = Log(log_type="Kick", member_id=member.id, \
                        responsible_id=ctx.message.author.id, \
                        reason=reason, date=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                if not ctx.message.server.id in self.servers_config["servers"]:
                    self.servers_config["servers"][ctx.message.server.id] = {}
                if not "logs" in self.servers_config["servers"][ctx.message.server.id]:
                    self.servers_config["servers"][ctx.message.server.id]["logs"] = {}
                if member.id in self.servers_config["servers"][ctx.message.server.id]["logs"]:
                    self.servers_config["servers"][ctx.message.server.id]["logs"][member.id].append(log) #pylint: disable=line-too-long
                else:
                    self.servers_config["servers"][ctx.message.server.id]["logs"][member.id] = [log]
                self.save_servers_config()
                await self.send_log(server=ctx.message.server, log=log)
                await self.bot.say("Done.")
            else:
                await self.bot.say("There's no member with such ID " + \
                                    "in this server.")
        except discord.Forbidden:
            await self.bot.say("I'm not allowed to do that.\n" + \
                                        "(Missing permissions)")

    @commands.command(pass_context=True)
    @checks.custom(is_owner_or_moderator)
    async def ban(self, ctx, member: discord.Member, days="0", *reason):
        """Bans a member
        Parameters:
            member: The member you want to ban from the server.
            days: The number of days worth of messages to delete from the member in the server.
                  Default value: 0 (which means that no messages from the member will be deleted).
                  Note: The minimum is 0 and the maximum is 7.
            *reason: The reason of the ban.

        Example: [p]ban @AMeanMember 3 He was very mean!
                 [p]ban @AnotherMeanMember 4
                 [p]ban @AnotherMeanMember Spaming cute cat pics
                 [p]ban @AnotherMeanMember"""
        try:
            days = int(days)
            to_add = ""
        except ValueError:
            to_add = days
            days = 0
        if days >= 0 and days <= 7:
            try:
                await self.bot.ban(member, days)
                reason = to_add + " ".join(reason)
                log = Log(log_type="Ban", member_id=member.id, \
                        responsible_id=ctx.message.author.id, \
                        reason=reason, date=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                if not ctx.message.server.id in self.servers_config["servers"]:
                    self.servers_config["servers"][ctx.message.server.id] = {}
                if not "logs" in self.servers_config["servers"][ctx.message.server.id]:
                    self.servers_config["servers"][ctx.message.server.id]["logs"] = {}
                if member.id in self.servers_config["servers"][ctx.message.server.id]["logs"]:
                    self.servers_config["servers"][ctx.message.server.id]["logs"][member.id].append(log) #pylint: disable=line-too-long
                else:
                    self.servers_config["servers"][ctx.message.server.id]["logs"][member.id] = [log]
                self.save_servers_config()
                await self.send_log(server=ctx.message.server, log=log)
                await self.bot.say("Done.")
            except discord.Forbidden:
                await self.bot.say("I'm not allowed to do that.\n" + \
                                    "(Missing permissions)")
        else:
            await self.bot.say("Incorrect days value.\n" + \
                "The minimum is 0 and the maximum is 7.")


    @commands.command(pass_context=True)
    @checks.custom(is_owner_or_moderator)
    async def ban_id(self, ctx, member_id: str, days="0", *reason):
        """Bans a member using his ID
        Parameters:
            member_id: The ID of the member you want to ban from the server.
            days: The number of days worth of messages to delete from the member in the server.
                  Default value: 0 (which means that no messages from the member will be deleted).
                  Note: The minimum is 0 and the maximum is 7.
            *reason: The reason of the ban.

        Example: [p]ban_id 346654353341546499 3 Bad guy.
                 [p]ban_id 346654353341546499 He shouldn't be here.
                 [p]ban_id 346654353341546499 4.
                 [p]ban_id 346654353341546499"""
        try:
            days = int(days)
            to_add = ""
        except ValueError:
            to_add = days
            days = 0
        if days >= 0 and days <= 7:
            member = discord.utils.find(lambda m: m.id == member_id, \
                                        ctx.message.server.members)
            if member:
                try:
                    await self.bot.ban(member, days)
                    reason = to_add + " ".join(reason)
                    log = Log(log_type="Ban", member_id=member.id, \
                            responsible_id=ctx.message.author.id, \
                            reason=reason, date=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                    if not ctx.message.server.id in self.servers_config["servers"]:
                        self.servers_config["servers"][ctx.message.server.id] = {}
                    if not "logs" in self.servers_config["servers"][ctx.message.server.id]:
                        self.servers_config["servers"][ctx.message.server.id]["logs"] = {}
                    if member.id in self.servers_config["servers"][ctx.message.server.id]["logs"]:
                        self.servers_config["servers"][ctx.message.server.id]["logs"][member.id].append(log) #pylint: disable=line-too-long
                    else:
                        self.servers_config["servers"][ctx.message.server.id]["logs"][member.id] = [log] #pylint: disable=line-too-long
                    self.save_servers_config()
                    await self.send_log(server=ctx.message.server, log=log)
                    await self.bot.say("Done.")
                except discord.Forbidden:
                    await self.bot.say("I'm not allowed to do that.\n" + \
                                        "(Missing permissions)")
            else:
                await self.bot.say("There's no member with such ID on this server.\n" + \
                        "You may be interested in the `[p]b1nzy_ban` command.")
        else:
            await self.bot.say("Incorrect days value.\n" + \
                "The minimum is 0 and the maximum is 7.")

    @commands.command(pass_context=True)
    @checks.custom(is_owner_or_moderator)
    async def b1nzy_ban(self, ctx, member_id: str, *reason):
        """Bans a member even if he's not on the server, using his ID
        Parameters:
            member_id: The ID of the member you want to ban.
            *reason: The reason of the ban.

        Example: [p]b1nzy_ban 346654353341546499 Bad guy.
                 [p]b1nzy_ban 346654353341546499

        Note: How does it works?
                If the member left the server to avoid the ban hammer, you
                can still use this command on him. He actually wouldn't be
                banned but as soon as he would come to the server again, he
                would be instantanely banned"""
        member = discord.utils.find(lambda m: m.id == member_id, \
                                    ctx.message.server.members)
        reason = " ".join(reason)
        if member:
            try:
                await self.bot.ban(member)
            except discord.Forbidden:
                await self.bot.say("I'm not allowed to do that.\n" + \
                                    "(Missing permissions)")
        else:
            if not ctx.message.server.id in self.b1nzy_banlist:
                self.b1nzy_banlist[ctx.message.server.id] = []
            if not member_id in self.b1nzy_banlist[ctx.message.server.id]:
                self.b1nzy_banlist[ctx.message.server.id].append(member_id)
                self.save_b1nzy_banlist()
            else:
                await self.bot.say("This user was already in the b1nzy banlist.")
                return

        log = Log(log_type="b1nzy ban", member_id=member_id, responsible_id=ctx.message.author.id, \
                        reason=reason, date=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        if not ctx.message.server.id in self.servers_config["servers"]:
            self.servers_config["servers"][ctx.message.server.id] = {}
        if not "logs" in self.servers_config["servers"][ctx.message.server.id]:
            self.servers_config["servers"][ctx.message.server.id]["logs"] = {}
        if member_id in self.servers_config["servers"][ctx.message.server.id]["logs"]:
            self.servers_config["servers"][ctx.message.server.id]["logs"][member_id].append(log) #pylint: disable=line-too-long
        else:
            self.servers_config["servers"][ctx.message.server.id]["logs"][member_id] = [log] #pylint: disable=line-too-long
        self.save_servers_config()
        await self.send_log(server=ctx.message.server, log=log)
        await self.bot.say("Done.")


    @commands.command(pass_context=True)
    @checks.custom(is_owner_or_moderator)
    async def unban(self, ctx, member: str, *reason):
        """Unbans a member
        Parameters:
            member: The member you want to unban from this server.
                    The format of this argument is Username#discriminator (see example).
            *reason: The reason of the unban.

        Example: [p]unban I'm not mean after all#1234
                 [p]unban AnInnocent#1234 He wasn't that mean."""
        member_info = member.split("#")
        if len(member_info) == 2:
            try:
                banned_members = await self.bot.get_bans(ctx.message.server)
                for banned in banned_members:
                    if banned.name == member_info[0] \
                            and banned.discriminator == member_info[1]:
                        member = banned
                        break
                if member:
                    await self.bot.unban(ctx.message.server, member)
                    reason = " ".join(reason)
                    log = Log(log_type="Unban", member_id=member.id, \
                            responsible_id=ctx.message.author.id, \
                            reason=reason, date=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                    if not ctx.message.server.id in self.servers_config["servers"]:
                        self.servers_config["servers"][ctx.message.server.id] = {}
                    if not "logs" in self.servers_config["servers"][ctx.message.server.id]:
                        self.servers_config["servers"][ctx.message.server.id]["logs"] = {}
                    if member.id in self.servers_config["servers"][ctx.message.server.id]["logs"]:
                        self.servers_config["servers"][ctx.message.server.id]["logs"][member.id].append(log) #pylint: disable=line-too-long
                    else:
                        self.servers_config["servers"][ctx.message.server.id]["logs"][member.id] = [log] #pylint: disable=line-too-long
                    self.save_servers_config()
                    await self.send_log(server=ctx.message.server, log=log)
                    await self.bot.say("Done.")
                else:
                    await self.bot.say("This user wasn't even banned here.")
            except discord.Forbidden:
                await self.bot.say("I'm not allowed to do that.\n" + \
                            "(Missing permissions")
        else:
            await self.bot.say("Incorrect format. Please check `[p]help unban`.")


    @commands.command(pass_context=True)
    @checks.custom(is_owner_or_moderator)
    async def unban_id(self, ctx, member_id: str, *reason):
        """Unbans a member using his ID
        Parameters:
            member_id: The ID of the member you want to unban from this server.
            *reason: The reason of the unban.

        Example: [p]unban_id 151661401411289088 I shouldn't have banned him, he's too cool.
                 [p]unban_id 151661401411289088"""
        try:
            banned = await self.bot.get_bans(ctx.message.server)
            member = discord.utils.find(lambda u: u.id == member_id, banned)
            if member:
                await self.bot.unban(ctx.message.server, member)
                reason = " ".join(reason)
                log = Log(log_type="Unban", member_id=member.id, \
                        responsible_id=ctx.message.author.id, \
                        reason=reason, date=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                if not ctx.message.server.id in self.servers_config["servers"]:
                    self.servers_config["servers"][ctx.message.server.id] = {}
                if not "logs" in self.servers_config["servers"][ctx.message.server.id]:
                    self.servers_config["servers"][ctx.message.server.id]["logs"] = {}
                if member.id in self.servers_config["servers"][ctx.message.server.id]["logs"]:
                    self.servers_config["servers"][ctx.message.server.id]["logs"][member.id].append(log) #pylint: disable=line-too-long
                else:
                    self.servers_config["servers"][ctx.message.server.id]["logs"][member.id] = [log]
                self.save_servers_config()
                await self.send_log(server=ctx.message.server, log=log)
                await self.bot.say("Done.")
            else:
                await self.bot.say("This user wasn't even banned here.")
        except discord.Forbidden:
            await self.bot.say("I'm not allowed to do that.\n" + \
                                "(Missing permissions")


    @commands.command(pass_context=True)
    @checks.custom(is_owner_or_moderator)
    async def list_logs(self, ctx, member: discord.Member):
        """Lists all the logs for a member of the server
        Parameters:
            member: The member you want to get the logs from.

        Example: [p]list_logs @Beafantles"""

        if ctx.message.server.id in self.servers_config["servers"] \
                and "logs" in self.servers_config["servers"][ctx.message.server.id] \
                and member.id in self.servers_config["servers"][ctx.message.server.id]["logs"]:
            msg = "```Markdown\nLogs for " + member.name + "#" + member.discriminator + \
                    "\n========================\n\n"
            i = 1
            for log in self.servers_config["servers"][ctx.message.server.id]["logs"][member.id]:
                msg += str(i) + ". " + log.type + "\n"
                msg += "\tCase#" + str(log.log_id) + "\n"
                msg += "\tResponsible: " + log.responsible.name + "#" + log.responsible.discriminator + " (" + log.responsible.id + ")\n" #pylint: disable=line-too-long
                msg += "\tReason: " + log.reason + "\n"
                msg += "\tDate: " + log.date + "\n\n"
                i += 1
            msg += "```"
            await self.bot.say(msg)
        else:
            await self.bot.say("No logs found for " + member.name + "#" + \
                    member.discriminator + " in this server.")


    @commands.command(pass_context=True)
    @checks.custom(is_owner_or_moderator)
    async def list_logs_id(self, ctx, member_id: str):
        """Lists all the logs for a member of the server using his ID
        Parameters:
            member_id: The ID of the member you want to get the logs from.

        Example: [p]list_logs_id 151661401411289088"""

        member = discord.utils.find(lambda m: m.id == member_id, \
                                    self.bot.get_all_members())
        if member:
            if ctx.message.server.id in self.servers_config \
                    and "logs" in self.servers_config["servers"][ctx.message.server.id] \
                    and member.id in self.servers_config["servers"][ctx.message.server.id]["logs"]:
                msg = "```Markdown\nLogs for " + member.name + "#" + member.discriminator + \
                        "\n========================\n\n"
                i = 1
                for log in self.servers_config["servers"][ctx.message.server.id]["logs"][member.id]:
                    msg += str(i) + ". " + log.type + "\n"
                    msg += "\tCase#" + str(log.log_id) + "\n"
                    msg += "\tResponsible: " + log.responsible.name + "#" + log.responsible.discriminator + " (" + log.responsible.id + ")\n" #pylint: disable=line-too-long
                    msg += "\tReason: " + log.reason + "\n"
                    msg += "\tDate: " + log.date + "\n\n"
                    i += 1
                msg += "```"
                await self.bot.say(msg)
            else:
                await self.bot.say("No logs found for " + member.name + "#" + \
                        member.discriminator + " in this server.")
        else:
            await self.bot.say("There's no member with such ID on this server.")


    async def check_new_comers(self, member):
        """Checks if a new comer is in the b1nzy banlist"""
        if member.server.id in self.b1nzy_banlist:
            if member.id in self.b1nzy_banlist[member.server.id]:
                try:
                    await self.bot.ban(member)
                    self.b1nzy_banlist[member.server.id].remove(member.id)
                    if not self.b1nzy_banlist[member.server.id]:
                        del self.b1nzy_banlist[member.server.id]
                    self.save_b1nzy_banlist()
                except discord.Forbidden:
                    await self.bot.send_message(member.server.owner, \
                        "Couldn't ban " + member.name + "#" + member.discriminator + \
                        " (" + member.id + ") who's in the b1nzy banlist --> missing permissions")
                except discord.HTTPException:
                    pass


def setup(bot):
    """Setup function"""
    mod = Admin(bot)
    bot.add_listener(mod.check_new_comers, "on_member_join")
    bot.add_cog(mod)
