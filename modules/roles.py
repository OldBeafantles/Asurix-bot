"""Roles module"""
import os
import re
from functools import partial
import copy
from modules.utils import checks
from modules.utils import utils
import discord
from discord.ext import commands




def free(roles, member: discord.Member):
    """Returns True"""
    #pylint: disable=unused-argument
    return True

def has_roles(roles, member: discord.Member):
    """Returns True if the member has all the roles"""
    member_roles = [x.id for x in member.roles]
    for role in roles:
        if not role in member_roles:
            return False
    return True

def has_not_roles(roles, member: discord.Member):
    """Returns True if the member hasn't any role in the roles argument"""
    for role in member.roles:
        if role.id in roles:
            return False
    return True

def has_any_roles(roles, member: discord.Member):
    """Returns True if the member has at least one of the roles argument"""
    member_roles = [x.id for x in member.roles]
    for role in roles:
        if role in member_roles:
            return True
    return False


CONDITIONS = { \
                "FREE": { \
                            "description": "The concerned roles can be self-assigned " + \
                                            "by anyone without any restriction.", \
                            "function": free \
                        }, \
                "HAS_ROLES": { \
                                "description": "The concerned roles can be self-assigned " + \
                                               "only if the user has some specific roles.", \
                                "function": has_roles \
                             }, \
                "HAS_NOT_ROLES": { \
                                    "description": "The concerned roles can be self-assigned " + \
                                                   "only if the user hasn't the specific roles.", \
                                    "function": has_not_roles \
                                 }, \
                "HAS_ANY_ROLES": { \
                                    "description": "The concerned roles can be self-assigned " + \
                                                   "only if the user has at least one of the " + \
                                                   "specific roles.", \
                                    "function": has_any_roles \
                                 }, \
             }


def is_owner_or_server_owner(ctx):
    """Returns true if the author is the owner of the server or the bot's owner"""
    return ctx.bot.is_owner(ctx.message.author.id) \
            or ctx.message.author.id == ctx.message.server.owner.id


class Roles:
    """Roles module"""

    def load_servers_config(self):
        """Loads the servers configuration"""
        if not os.path.exists(self.servers_config_file_path):

            if not os.path.isdir("data/roles"):
                os.makedirs("data/roles")

            utils.save_json(self.servers_config, self.servers_config_file_path)
        else:
            data = utils.load_json(self.servers_config_file_path)
            for server_id in data:
                self.servers_config[server_id] = {}
                for role_id in data[server_id]:
                    role = data[server_id][role_id]
                    self.servers_config[server_id][role_id] = role
                    assign_functions = []
                    for cond in role["assign-conditions"]:
                        assign_functions.append(partial(CONDITIONS[cond[0]]["function"], cond[1]))
                    self.servers_config[server_id][role_id]["assign-functions"] = assign_functions
                    removal_functions = []
                    for cond in role["removal-conditions"]:
                        removal_functions.append(partial(CONDITIONS[cond[0]]["function"], cond[1]))
                    self.servers_config[server_id][role_id]["removal-functions"] = removal_functions


    def save_servers_config(self):
        """Saves the servers configuration"""
        json_data = {}
        for server in self.servers_config:
            json_data[server] = {}
            for role_id in self.servers_config[server]:
                role_config = self.servers_config[server][role_id]
                json_data[server][role_id] = { \
                                        "assign-conditions": role_config["assign-conditions"], \
                                        "assign-expression": role_config["assign-expression"], \
                                        "removal-conditions": role_config["removal-conditions"], \
                                        "removal-expression": role_config["removal-expression"] \
                                          }
        utils.save_json(json_data, self.servers_config_file_path)


    def __init__(self, bot):
        """Init function"""
        self.bot = bot
        self.servers_config_file_path = "data/roles/servers.json"
        self.servers_config = {}
        self.load_servers_config()


    @commands.command()
    @checks.custom(is_owner_or_server_owner)
    async def list_roles_conditions(self):
        """Lists all the different conditions that can be used"""
        msg = "```Markdown\nList of the conditions\n======================\n\n"
        i = 1
        for cond in CONDITIONS:
            msg += str(i) + ". " + cond + "\n"
            msg += "\t" + CONDITIONS[cond]["description"] + "\n"
            i += 1
        msg += "```"
        await self.bot.say(msg)


    @commands.command(pass_context=True)
    @checks.custom(is_owner_or_server_owner)
    async def add_sa_role(self, ctx, *role_name):
        """Adds a role which could be self assignable
        Parameters:
            *role_name: The name of the role you want to be self-assignable.

        Example: [p]add_sa_role myRole"""
        role_name = " ".join(role_name)
        roles = [x.name for x in ctx.message.server.roles]
        if role_name in roles:
            role = discord.utils.find(lambda r: r.name == role_name, ctx.message.server.roles)
            if not (ctx.message.server.id in self.servers_config \
                    and role.id in self.servers_config[ctx.message.server.id]):
                bot = discord.utils.find(lambda m: m.id == self.bot.user.id, \
                                        ctx.message.server.members)
                perms = bot.server_permissions
                if perms.manage_roles and role.position <= bot.top_role.position:
                    if not ctx.message.server.id in self.servers_config:
                        self.servers_config[ctx.message.server.id] = {}
                    self.servers_config[ctx.message.server.id][role.id] = \
                        {"assign-conditions": [("FREE", [])], \
                         "assign-expression": "{0}", \
                         "assign-functions": [partial(CONDITIONS["FREE"]["function"], [])], \
                         "removal-conditions": [("FREE", [])], \
                         "removal-expression": "{0}", \
                         "removal-functions": [partial(CONDITIONS["FREE"]["function"], [])]}
                    self.save_servers_config()
                    await self.bot.say("Done! :ok_hand:")
                else:
                    await self.bot.say("Request cancelled. I wouldn't be able to assign this " + \
                                        "role (missing permissions).")
            else:
                await self.bot.say("This role is already self-assignable. You can check all " + \
                                "self-assignable roles by typing `[p]list_sa_roles`")
        else:
            await self.bot.say("There's no role with such name in this server.")


    @commands.command(pass_context=True)
    @checks.custom(is_owner_or_server_owner)
    async def list_sa_roles(self, ctx):
        """Lists all the self-assignable roles of the server"""
        if ctx.message.server.id in self.servers_config:
            msg = "```Markdown\nList of self-assignable roles\n====================\n\n"
            i = 1
            for role_id in self.servers_config[ctx.message.server.id]:
                role = discord.utils.find(lambda r, rid=role_id: r.id == rid, \
                                            ctx.message.server.roles)
                msg += str(i) + ". " + role.name + "\n"
                i += 1
            msg += "```\nTo get more details about a specific self-assignable role, you " + \
                "can use the command `[p]show_sa_role SELF_ASSIGNABLE_ROLE_NAME`."
            await self.bot.say(msg)
        else:
            await self.bot.say("There's no self-assignable roles in this server.")


    @commands.command(pass_context=True)
    @checks.custom(is_owner_or_server_owner)
    async def show_sa_role(self, ctx, *role_name):
        """Shows details about a self-assignable role
        Parameters:
            *role_name: The name of the self-assignable role you want details from.

        Example: [p]show_sa_role myRole"""
        if ctx.message.server.id in self.servers_config:
            role_name = " ".join(role_name)
            role = discord.utils.find(lambda r: r.name == role_name, ctx.message.server.roles)
            if role:
                if role.id in self.servers_config[ctx.message.server.id]:
                    msg = "```Markdown\n# " + role_name + "'s assign conditions\n"
                    role_config = self.servers_config[ctx.message.server.id][role.id]
                    i = 0
                    for cond in role_config["assign-conditions"]:
                        msg += "\t" + str(i) + ". " + cond[0] + "\t--> "
                        for cond_role_id in cond[1]:
                            cond_role = discord.utils.find(lambda x, c=cond_role_id: \
                                                    x.id == c, ctx.message.server.roles)
                            msg += cond_role.name + ", "
                        msg = msg[:-2] + "\n"
                        i += 1
                    msg += "\n# Expression: " + role_config["assign-expression"] + "\n\n"
                    i = 0
                    msg += "# " + role_name + "'s removal conditions\n"
                    for cond in role_config["removal-conditions"]:
                        msg += "\t" + str(i) + ". " + cond[0] + "\t--> "
                        for cond_role_id in cond[1]:
                            cond_role = discord.utils.find(lambda x, c=cond_role_id: \
                                                    x.id == c, ctx.message.server.roles)
                            msg += cond_role.name + ", "
                        msg = msg[:-2] + "\n"
                        i += 1
                    msg += "\n# Expression: " + role_config["removal-expression"] + "\n\n"
                    msg += "```"
                    await self.bot.say(msg)
                else:
                    await self.bot.say("There's no self-assignable role with such name for " + \
                        "this server.\nYou can check all self-assignable roles by typing " + \
                        "`[p]list_sa_roles`")
            else:
                await self.bot.say("There's no role with such name")
        else:
            await self.bot.say("There's no self-assignable roles in this server.")


    @commands.command(pass_context=True)
    @checks.custom(is_owner_or_server_owner)
    async def rem_sa_role(self, ctx, *role_name):
        """Removes a self-assignable role
        Parameters:
            *role_name: The name of the self-assignable role you want to remove.

        Example: [p]rem_sa_role myRole"""
        if ctx.message.server.id in self.servers_config:
            role_name = " ".join(role_name)
            role = discord.utils.find(lambda r: r.name == role_name, ctx.message.server.roles)
            if role:
                if role.id in self.servers_config[ctx.message.server.id]:
                    del self.servers_config[ctx.message.server.id][role.id]
                    if not self.servers_config[ctx.message.server.id]:
                        del self.servers_config[ctx.message.server.id]
                    self.save_servers_config()
                    await self.bot.say("Done! :ok_hand:")
                else:
                    await self.bot.say("There's no self-assignable role with such " + \
                                        "name on this server.")
            else:
                await self.bot.say("There is no role with such name on this server.")
        else:
            await self.bot.say("There's no self-assignable roles on this server.")


    @commands.command(pass_context=True)
    @checks.custom(is_owner_or_server_owner)
    async def edit_sa_expression(self, ctx, expression_type: str, *role_name):
        """Edits the expression used to check if someone can self-assign a role
        Parameters:
            expression_type: The type of expression you want to edit (assign or removal).
            *role_name: The name of the role you want to edit's assign expression.

        Example: [p]edit_sa_expression assign myRole
                 [p]edit_sa_expression removal myRole"""
        #pylint: disable=too-many-branches
        #pylint: disable=too-many-nested-blocks
        if ctx.message.server.id in self.servers_config:
            role_name = " ".join(role_name)
            role = discord.utils.find(lambda r: r.name == role_name, ctx.message.server.roles)
            if role:
                if role.id in self.servers_config[ctx.message.server.id]:
                    if expression_type == "removal" or expression_type == "assign":
                        role_config = self.servers_config[ctx.message.server.id][role.id]
                        msg = "```Markdown\n# " + role_name + "'s " + \
                                expression_type + " conditions\n"
                        i = 0
                        for cond in role_config[expression_type + "-conditions"]:
                            msg += "\t" + str(i) + ". " + cond[0] + "\t--> "
                            for cond_role_id in cond[1]:
                                cond_role = discord.utils.find(lambda x, c=cond_role_id: \
                                                        x.id == c, ctx.message.server.roles)
                                msg += cond_role.name + ", "
                            msg = msg[:-2] + "\n"
                            i += 1
                        msg += "\n# Current expression: " + \
                                role_config[expression_type + "-expression"] + "```\n"
                        msg += "Please type another expression:"
                        await self.bot.say(msg)
                        answer = await self.bot.wait_for_message(timeout=60, \
                                                                author=ctx.message.author, \
                                                                channel=ctx.message.channel)
                        if answer:
                            try:
                                #pylint: disable=W0123
                                new_expression = answer.content
                                expression_to_test = re.sub(r"{([0-9]*)}", r"{d[\1]}", new_expression) #pylint: disable=line-too-long
                                eval(expression_to_test.format( \
                                            d=role_config[expression_type + "-conditions"]))
                                role_config[expression_type + "-expression"] = new_expression
                                self.save_servers_config()
                                await self.bot.say("Done! :ok_hand:")
                            except ValueError:
                                await self.bot.say("This is not a valid expression.")
                            except NameError:
                                await self.bot.say("This is not a valid expression.")
                            except SyntaxError:
                                await self.bot.say("This is not a valid expression.")
                            except IndexError:
                                await self.bot.say("Incorrect index error.")
                        else:
                            await self.bot.say("I don't want to wait anymore, request cancelled.")
                    else:
                        await self.bot.say("Incorrect expression type, this must be `assign` " + \
                                                "or `removal`.")
                else:
                    await self.bot.say("There's no self-assignable role with such " + \
                                        "name on this server.")
            else:
                await self.bot.say("There is no role with such name on this server.")
        else:
            await self.bot.say("There's no self-assignable roles on this server.")


    @commands.command(pass_context=True)
    async def assign_role(self, ctx, *role_name):
        """Self-assigns a role
        Parameters:
            *role_name: The name of the role you want to get.

        Example: [p]assign_role myRole"""
        if ctx.message.server.id in self.servers_config:
            role_name = " ".join(role_name)
            role = discord.utils.find(lambda r: r.name == role_name, ctx.message.server.roles)
            if role:
                if role.id in self.servers_config[ctx.message.server.id]:
                    role_config = self.servers_config[ctx.message.server.id][role.id]
                    tests = []
                    for func in role_config["assign-functions"]:
                        tests.append(func(ctx.message.author))
                    #pylint: disable=W0123
                    expression = re.sub(r"{([0-9]*)}", r"{d[\1]}", role_config["assign-expression"])
                    if eval(expression.format(d=tests)):
                        try:
                            await self.bot.add_roles(ctx.message.author, role)
                            await self.bot.say("Done! :ok_hand:")
                        except discord.Forbidden:
                            await self.bot.say("I can't do that (missing permissions).")
                        except discord.HTTPException:
                            pass
                    else:
                        await self.bot.say("You don't respect the conditions to assign " + \
                                            "this role.")
                else:
                    await self.bot.say("There's no self-assignable role with such " + \
                                        "name on this server.")
            else:
                await self.bot.say("There is no role with such name on this server.")
        else:
            await self.bot.say("There's no self-assignable roles on this server.")

    @commands.command(pass_context=True)
    async def rem_role(self, ctx, *role_name):
        """Self-removes a role
        Parameters:
            *role_name: The name of the role you want to remove.

        Example: [p]rem_role myRole"""
        #pylint: disable=too-many-branches
        #pylint: disable=too-many-nested-blocks
        if ctx.message.server.id in self.servers_config:
            role_name = " ".join(role_name)
            role = discord.utils.find(lambda r: r.name == role_name, ctx.message.author.roles)
            if role:
                if role.id in self.servers_config[ctx.message.server.id]:
                    role_config = self.servers_config[ctx.message.server.id][role.id]
                    tests = []
                    for func in role_config["removal-functions"]:
                        tests.append(func(ctx.message.author))
                    #pylint: disable=W0123
                    expression = re.sub(r"{([0-9]*)}", r"{d[\1]}", role_config["removal-expression"]) #pylint: disable=line-too-long
                    if eval(expression.format(d=tests)):
                        try:
                            await self.bot.remove_roles(ctx.message.author, role)
                            await self.bot.say("Done! :ok_hand:")
                        except discord.Forbidden:
                            await self.bot.say("I can't do that (missing permissions).")
                        except discord.HTTPException:
                            pass
                    else:
                        await self.bot.say("You don't respect the conditions to remove " + \
                                        "this role.")
                else:
                    await self.bot.say("There's no self-assignable role with such " + \
                                        "name on this server.")
            else:
                await self.bot.say("You don't even have this role.")
        else:
            await self.bot.say("There's no self-assignable roles on this server.")


    @commands.command(pass_context=True)
    @checks.custom(is_owner_or_server_owner)
    async def add_sa_condition(self, ctx, condition_type: str, condition: str, *role_name):
        """Adds a condition for self-assignement/self-removal
        Parameters:
            condition_type: The type of condition you want to add (assign or removal).
            condition: The name of the condition you want to add.
            *role_name: The name of the role you want to add a condition to.

        Example: [p]add_sa_condition assign HAS_ROLES myRole
                 [p]add_sa_condition removal HAS_ANY_ROLES myRole"""
        #pylint: disable=too-many-branches
        #pylint: disable=too-many-nested-blocks
        if ctx.message.server.id in self.servers_config:
            role_name = " ".join(role_name)
            role = discord.utils.find(lambda r: r.name == role_name, ctx.message.server.roles)
            if role:
                if role.id in self.servers_config[ctx.message.server.id]:
                    if condition in CONDITIONS:
                        if condition_type == "removal" or condition_type == "assign":
                            await self.bot.say("Type all the roles concerned by this condition," + \
                                            " separated by ` <> `.\nExample: `Role 1 <> Role 2`")
                            answer = await self.bot.wait_for_message(author=ctx.message.author, \
                                                                    channel=ctx.message.channel, \
                                                                    timeout=60)
                            if answer:
                                roles_to_add_names = answer.content.split(" <> ")
                                roles_to_add_id = []
                                for role_to_test in roles_to_add_names:
                                    role_to_add = discord.utils.find(lambda r, rt=role_to_test: \
                                                            r.name == rt, ctx.message.server.roles)
                                    if role_to_add:
                                        roles_to_add_id.append(role_to_add.id)
                                    else:
                                        await self.bot.say("Incorrect roles.")
                                        return
                                self.servers_config[ctx.message.server.id][role.id][condition_type + "-conditions"].append((condition, roles_to_add_id)) #pylint: disable=line-too-long
                                self.servers_config[ctx.message.server.id][role.id][condition_type + "-functions"].append(partial(CONDITIONS[condition]["function"], roles_to_add_id)) #pylint: disable=line-too-long
                                self.save_servers_config()
                                await self.bot.say("Done! :ok_hand:")
                            else:
                                await self.bot.say("I don't want to wait anymore, " + \
                                                    "request cancelled.")
                        else:
                            await self.bot.say("Incorrect condition type, this must be " + \
                                                "`assign` or `removal`.")
                    else:
                        await self.bot.say("There's no such condition. To get the list of " + \
                            "all the available conditions, type `[p]list_roles_conditions`.")
                else:
                    await self.bot.say("There's no self-assignable role with such " + \
                                        "name on this server.")
            else:
                await self.bot.say("There is no role with such name on this server.")
        else:
            await self.bot.say("There's no self-assignable roles on this server.")


    @commands.command(pass_context=True)
    @checks.custom(is_owner_or_server_owner)
    async def rem_sa_condition(self, ctx, condition_type: str, *role_name):
        """Removes a condition for self-assignement
        Parameters:
            condition_type: The type of condition you want to remove (assign or removal).
            *role_name: The name of the role you want to remove a condition from.

        Example: [p]rem_sa_condition assign myRole
                 [p]rem_sa_condition removal myRole"""
        #pylint: disable=too-many-branches
        #pylint: disable=too-many-nested-blocks
        #pylint: disable=too-many-statements
        if ctx.message.server.id in self.servers_config:
            role_name = " ".join(role_name)
            role = discord.utils.find(lambda r: r.name == role_name, ctx.message.server.roles)
            if role:
                if role.id in self.servers_config[ctx.message.server.id]:
                    if condition_type == "removal" or condition_type == "assign":
                        role_config = copy.deepcopy(self.servers_config[ctx.message.server.id][role.id]) #pylint: disable=line-too-long
                        msg = "```Markdown\n# " + role_name + "'s " + \
                                condition_type + " conditions\n"
                        i = 0
                        for cond in role_config[condition_type + "-conditions"]:
                            msg += "\t" + str(i) + ". " + cond[0] + "\t--> "
                            for cond_role_id in cond[1]:
                                cond_role = discord.utils.find(lambda x, c=cond_role_id: \
                                                        x.id == c, ctx.message.server.roles)
                                msg += cond_role.name + ", "
                            msg = msg[:-2] + "\n"
                            i += 1
                        msg += "\n# Current expression: " + \
                                role_config[condition_type + "-expression"] + "```\n"
                        msg += "Please type the number of the condition you want to remove:"
                        await self.bot.say(msg)
                        answer = await self.bot.wait_for_message(timeout=60, \
                                                                author=ctx.message.author, \
                                                                channel=ctx.message.channel)
                        if answer:
                            try:
                                index = int(answer.content)
                                if index >= 0 and index <= len(role_config[condition_type + "-functions"]) - 1: #pylint:disable=line-too-long
                                    msg = ""
                                    if len(role_config[condition_type + "-functions"]) == 1:
                                        role_config[condition_type + "-functions"] = [partial(CONDITIONS["FREE"]["function"], [])] #pylint:disable=line-too-long
                                        role_config[condition_type + "-conditions"] = [("FREE", [])]
                                        msg += "The last condition will be remplaced by " + \
                                                "the `FREE` condition.\n"
                                    else:
                                        del role_config[condition_type + "-functions"][index]
                                        del role_config[condition_type + "-conditions"][index]
                                    msg += "Now, please type a new expression " + \
                                           "which respect the new conditions:"
                                    await self.bot.say(msg)
                                    new_expression = await self.bot.wait_for_message(timeout=60, \
                                                                        author=ctx.message.author, \
                                                                        channel=ctx.message.channel)
                                    if new_expression:
                                        try:
                                            #pylint: disable=W0123
                                            new_expression = new_expression.content
                                            expression = re.sub(r"{([0-9]*)}", r"{d[\1]}", new_expression) #pylint: disable=line-too-long
                                            eval(expression.format( \
                                                    d=role_config[condition_type + "-conditions"]))
                                            role_config[condition_type + "-expression"] = new_expression #pylint: disable=line-too-long
                                            self.servers_config[ctx.message.server.id][role.id] = role_config #pylint: disable=line-too-long
                                            self.save_servers_config()
                                            await self.bot.say("Done! :ok_hand:")
                                        except ValueError:
                                            await self.bot.say("This is not a valid expression.")
                                        except NameError:
                                            await self.bot.say("This is not a valid expression.")
                                        except SyntaxError:
                                            await self.bot.say("This is not a valid expression.")
                                        except IndexError:
                                            await self.bot.say("Incorrect index error.")
                                    else:
                                        await self.bot.say("I don't want to wait anymore, " + \
                                                            "request cancelled.")
                                else:
                                    await self.bot.say("Please type a correct number.")
                            except ValueError:
                                await self.bot.say("This is not a number.")
                        else:
                            await self.bot.say("I don't want to wait anymore, request cancelled.")
                    else:
                        await self.bot.say("Incorrect condition type, this must be " + \
                                            "`assign` or `removal`.")
                else:
                    await self.bot.say("There's no self-assignable role with such " + \
                                        "name on this server.")
            else:
                await self.bot.say("There is no role with such name on this server.")
        else:
            await self.bot.say("There's no self-assignable roles on this server.")


def setup(bot):
    """Setup function"""
    bot.add_cog(Roles(bot))
