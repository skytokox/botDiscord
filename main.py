import datetime
import logging
import discord
from discord.ext import commands
import csv
from urllib import request

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

token = 'OTA0Nzk0MDEyMTQ0MjQ2Nzk1.YYAtFg.H5O-JqTQVHnmzWm5JccGpTXBZ7Y'

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
async def pobierzdane(ctx):
    url = "https://www.arcgis.com/sharing/rest/content/items/6ff45d6b5b224632a672e764e04e8394/data"
    date = datetime.datetime.now()
    local_file = f'dane_powiat_{date.strftime("%d")}.{date.strftime("%m")}.{date.strftime("%Y")}.csv'
    request.urlretrieve(url, f'./covid/{local_file}')
@bot.command()
async def covid(ctx, location: str = None, string: str = None):
    if string is None:
        date = datetime.datetime.now()
    else:
        test = string.split('.')
        if int(test[0]) <= 31:
            date = datetime.datetime(int(test[2]), int(test[1]), int(test[0]))
        else:
            date = datetime.datetime(int(test[0]), int(test[1]), int(test[2]))

    if location is None:
        location = "Cały kraj"

    dateWEEKAgo = date - datetime.timedelta(weeks=1)
    with open(f'./covid/dane_powiat_{date.strftime("%d")}.{date.strftime("%m")}.{date.strftime("%Y")}.csv',
              'r') as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            if location == row[1]:
                ilosc_zakazen = row[2]
                ilosc_zakazen_100k = round(float(row[3]) * 10, 1)
                ilosc_zgonow = row[4]
                ilosc_zgonowCOVID = row[5]
                ilosc_zgonowZCOVID = row[6]
                ilosc_kwarantanna = row[9]
                ilosc_testow = row[10]
                ilosc_pozytywnych_testow = round(int(row[2]) / int(row[10]) * 100, 1)

    with open(
            f'./covid/dane_powiat_{dateWEEKAgo.strftime("%d")}.{dateWEEKAgo.strftime("%m")}.{dateWEEKAgo.strftime("%Y")}.csv',
            'r') as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            if location == row[1]:
                ilosc_zakazen_WA = row[2]
                ilosc_zgonow_WA = row[4]
                ilosc_testow_WA = row[10]
                ilosc_pozytywnych_testow_WA = round(int(row[2]) / int(row[10]) * 100, 1)
    embed = discord.Embed(
        title="COVID-19",
        description="Dzisiejsze statystyki COVID-19 od Ministerstwa Zdrowia",
        color=discord.Color.purple()
    )
    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1069885833656844290/Inl2pghx_400x400.jpg")

    if int(ilosc_zakazen) - int(ilosc_zakazen_WA) > 0:
        embed.add_field(name="Ilość zakażeń:",
                        value=f'{ilosc_zakazen}, wzrost o {int(ilosc_zakazen) - int(ilosc_zakazen_WA)}({round((int(ilosc_zakazen) / int(ilosc_zakazen_WA) - 1) * 100, 1)}%)',inline=True)
    else:
        embed.add_field(name="Ilość zakażeń:",
                        value=f'{ilosc_zakazen}, spadek o {int(ilosc_zakazen_WA) - int(ilosc_zakazen)}({round((int(ilosc_zakazen) / int(ilosc_zakazen_WA) - 1) * 100, 1)}%)',
                        inline=True)

    if ilosc_zakazen_100k < 10:
        embed.add_field(name="Ilość zakażeń na 100k:", value=f'{ilosc_zakazen_100k} :green_circle:', inline=True)
    elif 10 <= ilosc_zakazen_100k < 25:
        embed.add_field(name="Ilość zakażeń na 100k:", value=f'{ilosc_zakazen_100k} :yellow_circle:', inline=True)
    elif 25 <= ilosc_zakazen_100k < 50:
        embed.add_field(name="Ilość zakażeń na 100k:", value=f'{ilosc_zakazen_100k} :red_circle:', inline=True)
    elif 50 <= ilosc_zakazen_100k < 70:
        embed.add_field(name="Ilość zakażeń na 100k:", value=f'{ilosc_zakazen_100k} :purple_circle:', inline=True)
    elif 70 <= ilosc_zakazen_100k < 100:
        embed.add_field(name="Ilość zakażeń na 100k:", value=f'{ilosc_zakazen_100k} :brown_circle:', inline=True)

    if int(ilosc_zgonow) - int(ilosc_zgonow_WA) > 0 and int(ilosc_zgonow_WA) != 0:
        embed.add_field(name="Ilość zgonów:",
                        value=f'{ilosc_zgonow}, wzrost o {int(ilosc_zgonow) - int(ilosc_zgonow_WA)}({round((int(ilosc_zgonow) / int(ilosc_zgonow_WA) - 1) * 100, 1)}%)',
                        inline=False)
    elif int(ilosc_zgonow) - int(ilosc_zgonow_WA) == 0:
        embed.add_field(name="Ilość zgonów:", value=f'{ilosc_zgonow}, brak wzrostu', inline=False)
    elif int(ilosc_zgonow_WA) == 0:
        embed.add_field(name="Ilość zgonów:",
                        value=f'{ilosc_zgonow}, wzrost o {int(ilosc_zgonow) - int(ilosc_zgonow_WA)}({round((int(ilosc_zgonow) / 1) * 100, 1)}%)',
                        inline=False)
    else:
        embed.add_field(name="Ilość zgonów:",
                        value=f'{ilosc_zgonow}, spadek o {int(ilosc_zgonow_WA) - int(ilosc_zgonow)}({round((int(ilosc_zgonow) / int(ilosc_zgonow_WA) - 1) * 100, 1)}%)',
                        inline=False)

    embed.add_field(name="Zgony z powodu \nCOVID-19", value=ilosc_zgonowCOVID, inline=True)
    embed.add_field(name="Zgony z chorobami współistniejacymi:", value=ilosc_zgonowZCOVID, inline=True)
    embed.add_field(name="Liczba osób na kwarantannie:", value=f'{ilosc_kwarantanna}', inline=False)

    if int(ilosc_testow) - int(ilosc_testow_WA) > 0:
        embed.add_field(name="Liczba wykonanych testów:",
                        value=f'{ilosc_testow}, wzrost o {int(ilosc_testow) - int(ilosc_testow_WA)}({round((int(ilosc_testow) / int(ilosc_testow_WA) - 1) * 100, 1)}%)',
                        inline=True)
    else:
        embed.add_field(name="Liczba wykonanych testów:",
                        value=f'{ilosc_testow}, spadek o {int(ilosc_testow_WA) - int(ilosc_testow)}({round((int(ilosc_testow) / int(ilosc_testow_WA) - 1) * 100, 1)}%)',
                        inline=True)

    if int(ilosc_pozytywnych_testow) - int(ilosc_pozytywnych_testow_WA) > 0:
        embed.add_field(name="Liczba pozytywnych testow:",
                        value=f'{ilosc_pozytywnych_testow}%, wzrost o {int(ilosc_pozytywnych_testow) - int(ilosc_pozytywnych_testow_WA)}%',
                        inline=True)
    else:
        embed.add_field(name="Liczba pozytywnych testow:",
                        value=f'{ilosc_pozytywnych_testow}%, spadek o {int(ilosc_pozytywnych_testow_WA) - int(ilosc_pozytywnych_testow)}%',
                        inline=True)
    if date.strftime("%d") == datetime.datetime.now().strftime("%d"):
        embed.description = "Dzisiejsze statystyki COVID-19 od Ministerstwa Zdrowia"
    else:
        embed.description = f'Statystyki COVID-19 na dzień: {date.strftime("%d")}.{date.strftime("%m")}.{date.strftime("%Y")}'

    await ctx.send(embed=embed)


bot.run(token)
