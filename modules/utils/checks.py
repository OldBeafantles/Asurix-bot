"""Checking utilities file"""
from discord.ext import commands

def is_owner_check(ctx):
    """Checks if it's the owner or not"""
    return ctx.bot.is_owner(ctx.message.author.id)

def is_owner_or_server_owner_check(ctx):
    """Returns true if it's the bot's owner or server owner"""
    return ctx.bot.is_owner(ctx.message.author.id) \
            or ctx.message.author.id == ctx.message.server.owner.id

def is_owner():
    """Checks if it's the owner or not"""
    return commands.check(is_owner_check)

def  is_owner_or_server_owner():
    """Returns true if it's the bot's owner or server owner"""
    return commands.check(is_owner_or_server_owner_check)

def custom(function):
    """Custom check"""
    return commands.check(function)
