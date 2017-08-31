"""Admin module"""
import os
import discord
from discord.ext import commands
from modules.utils import checks
from modules.utils import utils


class Admin:
    """Admin module"""

    def load_config(self):
        """Loads the configuration"""
        if not os.path.exists(self.servers_config_file_path):

            if not os.path.isdir("data/admin"):
                os.makedirs("data/admin")

            utils.save_json(self.servers_config, self.servers_config_file_path)
        else:
            self.servers_config = utils.load_json(self.servers_config_file_path)


    def __init__(self, bot):
        """Init function"""
        self.bot = bot
        self.servers_config = {}
        self.servers_config_file_path = "data/admin/servers_config.json"
        self.load_config()


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
                    self.servers_config[ctx.message.server.id]["log channel id"] = channel.id
                    utils.save_json(self.servers_config, self.servers_config_file_path)
                    await self.bot.say("Done. :ok_hand:")
                else:
                    await self.bot.say("I'm not allowed to send messages there.\n" + \
                                        "(Missing permissions)")
            else:
                if ctx.message.server.id in self.servers_config:
                    del self.servers_config[ctx.message.server.id]["log channel id"]
                    utils.save_json(self.servers_config, self.servers_config_file_path)
                await self.bot.say("Done! :ok_hand:")


    @commands.command()
    @checks.is_owner_or_has_permissions(["kick"])
    async def kick(self, member: discord.Member):
        """Kicks a member
        Parameters:
            member: The member you want to kick.

        Example: [p]kick @ABadGuy"""
        try:
            await self.bot.kick(member)
            await self.bot.say("Done.")
        except discord.Forbidden:
            await self.bot.say("I'm not allowed to do that.\n" + \
                                        "(Missing permissions)")


    @commands.command(pass_context=True)
    @checks.is_owner_or_has_permissions(["kick"])
    async def kick_id(self, ctx, member_id: str):
        """Kicks a member using his ID
        Parameters:
            member_id: The ID of member you want to kick.

        Example: [p]kick_id 346654353341546499"""
        try:
            member = discord.utils.find(lambda m: m.id == member_id, \
                                        ctx.message.server.members)
            if member:
                await self.bot.kick(member)
                await self.bot.say("Done.")
            else:
                await self.bot.say("There's no member with such ID " + \
                                    "in this server.")
        except discord.Forbidden:
            await self.bot.say("I'm not allowed to do that.\n" + \
                                        "(Missing permissions)")

    @commands.command()
    @checks.is_owner_or_has_permissions(["ban"])
    async def ban(self, member: discord.Member, days=0):
        """Bans a member
        Parameters:
            member: The member you want to ban from the server.
            days: The number of days worth of messages to delete from the member in the server.
                  Default value: 0 (which means that no messages from the member will be deleted).
                  Note: The minimum is 0 and the maximum is 7.

        Example: [p]ban @AMeanMember 3
                 [p]ban @AnotherMeanMember"""
        if days >= 0 and days <= 7:
            try:
                await self.bot.ban(member, days)
                await self.bot.say("Done.")
            except discord.Forbidden:
                await self.bot.say("I'm not allowed to do that.\n" + \
                                    "(Missing permissions)")
        else:
            await self.bot.say("Incorrect days value.\n" + \
                "The minimum is 0 and the maximum is 7.")


    @commands.command(pass_context=True)
    @checks.is_owner_or_has_permissions(["ban"])
    async def ban_id(self, ctx, member_id: str, days=0):
        """Bans a member using his ID
        Parameters:
            member_id: The ID of the member you want to ban from the server.
            days: The number of days worth of messages to delete from the member in the server.
                  Default value: 0 (which means that no messages from the member will be deleted).
                  Note: The minimum is 0 and the maximum is 7.

        Example: [p]ban_id 346654353341546499 3
                 [p]ban_id 346654353341546499"""
        if days >= 0 and days <= 7:
            member = discord.utils.find(lambda m: m.id == member_id, \
                                        ctx.message.server.members)
            if member:
                try:
                    await self.bot.ban(member, days)
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
    @checks.is_owner_or_has_permissions(["ban"])
    async def unban(self, ctx, member: str):
        """Unbans a member
        Parameters:
            member: The member you want to unban from this server.
                    The format of this argument is Username#discriminator (see example).

        Example: [p]unban I'm not mean after all#1234"""
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
                    await self.bot.say("Done.")
                else:
                    await self.bot.say("This user wasn't even banned here.")
            except discord.Forbidden:
                await self.bot.say("I'm not allowed to do that.\n" + \
                            "(Missing permissions")
        else:
            await self.bot.say("Incorrect format. Please check `[p]help unban`.")


    @commands.command(pass_context=True)
    @checks.is_owner_or_has_permissions(["ban"])
    async def unban_id(self, ctx, member_id: str):
        """Unbans a member using his ID
        Parameters:
            member_id: The ID of the member you want to unban from this server.

        Example: [p]unban_id 151661401411289088"""
        try:
            banned = await self.bot.get_bans(ctx.message.server)
            member = discord.utils.find(lambda u: u.id == member_id, banned)
            if member:
                await self.bot.unban(ctx.message.server, member)
                await self.bot.say("Done.")
            else:
                await self.bot.say("This user wasn't even banned here.")
        except discord.Forbidden:
            await self.bot.say("I'm not allowed to do that.\n" + \
                                "(Missing permissions")


def setup(bot):
    """Setup function"""
    bot.add_cog(Admin(bot))
