"""Checking utilities file"""
from discord.ext import commands

PERMISSIONS = { \
                "create instant invite": lambda p: p.create_instant_invite, \
                "ban": lambda p: p.ban_members, \
                "kick": lambda p: p.kick_members, \
                "admin": lambda p: p.administrator, \
                "manage channels": lambda p: p.manage_channels, \
                "manage server": lambda p: p.manage_server, \
                "add reactions": lambda p: p.add_reactions, \
                "view audit logs": lambda p: p.view_audit_logs, \
                "read messages": lambda p: p.read_messages, \
                "send messages": lambda p: p.send_messages, \
                "send tts messages": lambda p: p.send_tts_messages, \
                "manage messages": lambda p: p.manage_messages, \
                "embed links": lambda p: p.embed_links, \
                "attach files": lambda p: p.attach_files, \
                "read message history": lambda p: p.read_message_history, \
                "mention everyone": lambda p: p.mention_everyone, \
                "external emojis": lambda p: p.external_emojis, \
                "connect": lambda p: p.connect, \
                "speak": lambda p: p.speak, \
                "mute members": lambda p: p.mute_members, \
                "deafen members": lambda p: p.deafen_members, \
                "move members": lambda p: p.move_members, \
                "use voice activation": lambda p: p.use_voice_activation, \
                "change nickname": lambda p: p.change_nickname, \
                "manage nicknames": lambda p: p.manage_nicknames, \
                "manage roles": lambda p: p.manage_roles, \
                "manage webhooks": lambda p: p.manage_webhooks, \
                "manage emojis": lambda p: p.manage_emojis \
              }


def is_owner_check(ctx):
    """Checks if it's the owner or not"""
    return ctx.bot.owner_id == ctx.message.author.id


def is_owner_or_server_owner_check(ctx):
    """Returns true if it's the bot's owner or server owner"""
    return ctx.bot.owner_id == ctx.message.author.id \
            or ctx.message.author.id == ctx.message.server.owner.id


def is_owner_or_has_permissions_check(ctx, permissions):
    """Returns true if it's the bot's owner or if the member has the permissions"""
    #pylint: disable=invalid-name
    for perm in permissions:
        if perm not in PERMISSIONS:
            return False
        else:
            if not PERMISSIONS[perm](ctx.message.author.server_permissions):
                return False
    return True


def is_owner_or_administrator_check(ctx):
    """Returns true if it's the bot's owner or if the member is an administator"""
    return ctx.message.author.id == ctx.bot.owner_id \
        or ctx.message.author.server_permissions.administrator


def is_owner():
    """Checks if it's the owner or not"""
    return commands.check(is_owner_check)


def is_owner_or_server_owner():
    """Returns true if it's the bot's owner or server owner"""
    return commands.check(is_owner_or_server_owner_check)


def is_owner_or_administrator():
    """Returns true if it's the bot's owner or if the member is an administator"""
    return commands.check(is_owner_or_administrator_check)


def is_owner_or_has_permissions(permissions):
    """Returns true if it's the bot's owner or if the member has the permissions"""
    def check(ctx):
        """Simple checking function"""
        return is_owner_or_has_permissions_check(ctx, permissions)
    return commands.check(check)


def is_owner_or_has_permission(permission):
    """Returns true if it's the bot's owner or if the member has the permission"""
    def check(ctx):
        """Simple checking function"""
        if permission not in PERMISSIONS:
            return False
        return PERMISSIONS[permission](ctx.message.author.server_permissions)
    return commands.check(check)


def custom(function):
    """Custom check"""
    return commands.check(function)
