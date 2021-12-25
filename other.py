import datetime
import discord
from discord.ext import commands, tasks


class Other(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def nub(self, ctx, user: discord.Member = None):
        if user is None:
            if str(ctx.author) == ".sky#9999":
                await ctx.send(f'{ctx.author} nie jest nubem')
            else:
                await ctx.send(f'{ctx.author} jest nubem')
        if str(user) == "piotreee#9595":
            await ctx.send(f'{user} jest nubem')
        else:
            await ctx.send(f'{user} nie jest nubem')

    @commands.command()
    async def avatar(self, ctx, user: discord.Member = None):
        if user is None:
            await ctx.send(f'Avatar uzytkownika: {ctx.author}')
            await ctx.send(ctx.author.avatar_url)
        else:
            await ctx.send(f'Avatar uzytkownika: {user}')
            await ctx.send(user.avatar_url)

    @commands.command()
    async def time(self, ctx):
        await ctx.send(datetime.datetime.now())

    @commands.command()
    async def ping(self, ctx):
        t = await ctx.send('Pong!')
        ping = (t.created_at - ctx.message.created_at).microseconds / 1000
        await t.edit(content=f'Pong! - ping wynosi {ping}ms')


def setup(bot):
    bot.add_cog(Other(bot))
