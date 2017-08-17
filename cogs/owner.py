import discord
import traceback
from discord.ext import commands
from .utils import checks
import textwrap
import inspect
import asyncio
import io
from contextlib import redirect_stdout


class Owner:
    """Owner commands"""

    def __init__(self, bot):
        self.bot = bot
        self.last_result = None
        self.sessions = set()


    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')


    def get_syntax_error(self, e):
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'


    @commands.command(pass_context=True, hidden=True, name='eval')
    @checks.is_owner()
    async def eval(self, ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.message.channel,
            'author': ctx.message.author,
            'server': ctx.message.server,
            'message': ctx.message,
            '_': self.last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await self.bot.say(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await self.bot.say(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await self.bot.say(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await self.bot.say(f'```py\n{value}{ret}\n```')

    @commands.command(pass_context=True, hidden=True)
    @checks.is_owner()
    async def repl(self, ctx):
        """Launches an interactive REPL session."""
        variables = {
            'ctx': ctx,
            'bot': self.bot,
            'message': ctx.message,
            'server': ctx.message.server,
            'channel': ctx.message.channel,
            'author': ctx.message.author,
            '_': None,
        }

        if ctx.message.channel.id in self.sessions:
            await self.bot.say('Already running a REPL session in this channel. Exit it with `quit`.')
            return

        self.sessions.add(ctx.message.channel.id)
        await self.bot.say('Enter code to execute or evaluate. `exit()` or `quit` to exit.')

        def check(m):
            return m.author.id == ctx.message.author.id and \
                   m.channel.id == ctx.message.channel.id and \
                   m.content.startswith('`')

        while True:
            try:
                response = await self.bot.wait_for_message(check = check, timeout = 10.0 * 60.0)
            except asyncio.TimeoutError:
                await self.bot.say('Exiting REPL session.')
                self.sessions.remove(ctx.message.channel.id)
                break

            cleaned = self.cleanup_code(response.content)

            if cleaned in ('quit', 'exit', 'exit()'):
                await self.bot.say('Exiting.')
                self.sessions.remove(ctx.message.channel.id)
                return

            executor = exec
            if cleaned.count('\n') == 0:
                # single statement, potentially 'eval'
                try:
                    code = compile(cleaned, '<repl session>', 'eval')
                except SyntaxError:
                    pass
                else:
                    executor = eval

            if executor is exec:
                try:
                    code = compile(cleaned, '<repl session>', 'exec')
                except SyntaxError as e:
                    await self.bot.say(self.get_syntax_error(e))
                    continue

            variables['message'] = response

            fmt = None
            stdout = io.StringIO()

            try:
                with redirect_stdout(stdout):
                    result = executor(code, variables)
                    if inspect.isawaitable(result):
                        result = await result
            except Exception as e:
                value = stdout.getvalue()
                fmt = f'```py\n{value}{traceback.format_exc()}\n```'
            else:
                value = stdout.getvalue()
                if result is not None:
                    fmt = f'```py\n{value}{result}\n```'
                    variables['_'] = result
                elif value:
                    fmt = f'```py\n{value}\n```'

            try:
                if fmt is not None:
                    if len(fmt) > 2000:
                        await self.bot.say('Content too big to be printed.')
                    else:
                        await self.bot.say(fmt)
            except discord.Forbidden:
                pass
            except discord.HTTPException as e:
                await self.bot.say(f'Unexpected error: `{e}`')

    @commands.command()
    @checks.is_owner()
    async def load(self, module : str):
        """Loads a module."""
        try:
            self.bot.load_extension("cogs." + module)
        except Exception as e:
            await self.bot.say('\U0001f52b')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say('\U0001f44c')


    @commands.command()
    @checks.is_owner()
    async def unload(self, module : str):
        """Unloads a module."""
        try:
            self.bot.unload_extension("cogs." + module)
        except Exception as e:
            await self.bot.say('\U0001f52b')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say('\U0001f44c')

    @commands.command()
    @checks.is_owner()
    async def reload(self, module : str):
        """Reloads a module."""
        try:
            self.bot.unload_extension("cogs." + module)
            self.bot.load_extension("cogs." + module)
        except Exception as e:
            await self.bot.say('\U0001f52b')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say('\U0001f44c')


def setup(bot):
    bot.add_cog(Owner(bot))