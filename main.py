
import datetime
import logging
import discord
from discord.ext import commands, tasks
from config import token
import time


# date = datetime.datetime.today()
# date_str = date.strftime("_%d.%m.%Y")
# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(filename=f'./logs/discord{date_str}.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)

bot = commands.Bot(command_prefix="!", help_command=None)



@bot.event
async def on_ready():
    print("Zalogowano jako: " + bot.user.name)


bot.load_extension('covid')
bot.load_extension('omicron')
bot.load_extension('papiez')
bot.load_extension('other')
bot.run(token)
