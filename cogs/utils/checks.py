from discord.ext import commands

def is_owner_check(ctx):
    return ctx.bot.is_owner(ctx.message.author.id)

def is_owner():
    return commands.check(is_owner_check)