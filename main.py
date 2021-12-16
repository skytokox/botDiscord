import asyncio
import datetime
import logging
import re
import discord
from discord.ext import commands, tasks
import csv
from urllib import request
from urllib.request import urlopen
from zipfile import ZipFile
# from config import token
from bs4 import BeautifulSoup
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

urlCOVID = "https://www.arcgis.com/sharing/rest/content/items/6ff45d6b5b224632a672e764e04e8394/data"
urlVACCINES = "https://www.arcgis.com/sharing/rest/content/items/3f47db945aff47e582db8aa383ccf3a1/data"
urlVARIANTS = "https://newsnodes.com/omicron_tracker#"

local_file_COVID = f'dane_powiat{date_str}.csv'
local_file_VACCINES = f'szczepienia{date_str}.zip'
local_file_VARIANTS = f'warianty{date_str}.csv'
request.urlretrieve(urlCOVID, f'./covid/{local_file_COVID}')
request.urlretrieve(urlVACCINES, f'./szczepienia/zip/{local_file_VACCINES}')

page = urlopen(urlVARIANTS)
soup = BeautifulSoup(page, 'html.parser')
content = soup.find('img', {'src': "/images/flagsxs/PL.png"})
content_parent = content.parent.parent
totalOmicronCount = int(content_parent.find('td', {"class": "u-text-r"}).text)
newOmicronCasesTXT = content_parent.find('span', {"style": "font-size: 9px"}).text
newOmicronCases = int(re.search(r'\d+', newOmicronCasesTXT).group())
zipdata = ZipFile(date.strftime('./szczepienia/zip/szczepienia_%d.%m.%Y.zip'), 'r')
zipinfos = zipdata.infolist()
for zipinfo in zipinfos:
    if 'rap_rcb_global_szczepienia.csv' in zipinfo.filename:
        zipinfo.filename = f'./szczepienia/csv/{date.strftime("szczepienia_%d.%m.%Y.csv")}'
        zipdata.extract(zipinfo)

x = 5


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
bot.run(token)
