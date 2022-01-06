import datetime
import random
import version
import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter


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

    @commands.command()
    async def choose(self, ctx, *, content):
        options = content.split('/')
        selected = random.choice(options)
        await ctx.send(f'Wybrałem {selected}!')

    @commands.command()
    async def help(self, ctx):
        color = [int(random.random() * 255), int(random.random() * 255), int(random.random() * 255)]
        sky = await MemberConverter().convert(ctx, "351007376779771904")
        avek_skaja = sky.avatar_url
        embed = discord.Embed(
            title='Cloudy',
            description='Informacje na temat komend w bocie',
            color=discord.Color.from_rgb(color[0], color[1], color[2])
        )
        embed.add_field(name='Ogólne', value="Ogólne komendy", inline=False)
        embed.add_field(name='!avatar', value='Pokazuje avatar użytkownika, prawidłowe użycie !avatar <ping>',
                        inline=False)
        embed.add_field(name='!time', value='Pokazuje czas na hoscie bota, prawidłowe użycie !time', inline=False)
        embed.add_field(name='!ping', value='Pokazuje ping bota, prawidłowe użycie !ping', inline=False)
        embed.add_field(name='!choose', value='Wybiera jedną z opcji, prawidłowe użycie !choose opcja1/opcja2/opcja3',
                        inline=False)
        embed.add_field(name='COVID', value="Komendy związane z COVID", inline=False)
        embed.add_field(name='!covid', value='Pokazuje dzisiejsze statystki dla całego kraju, prawidłowe użycie !covid')
        embed.set_footer(text=f'Bot stworzony przez {sky.name}#{sky.discriminator}, Wersja {version.bot_version}', icon_url=avek_skaja)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Other(bot))
