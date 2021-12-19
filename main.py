
import datetime
import logging
import discord
from discord.ext import commands, tasks
# from config import token
import os
token = os.environ.get('BOT_TOKEN')

date = datetime.datetime.today()
date_str = date.strftime("_%d.%m.%Y")
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=f'./logs/discord{date_str}.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix="!")



@bot.event
async def on_ready():
    print("Zalogowano jako: " + bot.user.name)




@bot.command()
async def nub(ctx, user: discord.Member = None):
    if user is None:
        if str(ctx.author) == ".sky#9999":
            await ctx.send(f'{ctx.author} nie jest nubem')
        else:
            await ctx.send(f'{ctx.author} jest nubem')
    if str(user) == "piotreee#9595":
        await ctx.send(f'{user} jest nubem')
    else:
        await ctx.send(f'{user} nie jest nubem')


@bot.command()
async def avatar(ctx, user: discord.Member = None):
    if user is None:
        await ctx.send(f'Avatar uzytkownika: {ctx.author}')
        await ctx.send(ctx.author.avatar_url)
    else:
        await ctx.send(f'Avatar uzytkownika: {user}')
        await ctx.send(user.avatar_url)

@bot.command()
async def time(ctx):
    await ctx.send(datetime.datetime.now())


bot.load_extension('covid')
bot.load_extension('omicron')
bot.run(token)
