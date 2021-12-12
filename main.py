import datetime
import logging

import discord
from discord.ext import commands
import csv
from urllib import request
from zipfile import ZipFile
from config import token

date = datetime.datetime.today()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=f'./logs/discord{date.strftime("_%d.%m.%Y")}.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


bot = commands.Bot(command_prefix="!")

urlCOVID = "https://www.arcgis.com/sharing/rest/content/items/6ff45d6b5b224632a672e764e04e8394/data"
urlVACCINES = "https://www.arcgis.com/sharing/rest/content/items/3f47db945aff47e582db8aa383ccf3a1/data"

local_file_COVID = f'dane_powiat_{date.strftime("%d.%m.%Y")}.csv'
local_file_VACCINES = f'szczepienia_{date.strftime("%d.%m.%Y")}.zip'
request.urlretrieve(urlCOVID, f'./covid/{local_file_COVID}')
request.urlretrieve(urlVACCINES, f'./szczepienia/zip/{local_file_VACCINES}')



zipdata = ZipFile(date.strftime('./szczepienia/zip/szczepienia_%d.%m.%Y.zip'), 'r')
zipinfos = zipdata.infolist()
for zipinfo in zipinfos:
    if 'rap_rcb_global_szczepienia.csv' in zipinfo.filename:
        zipinfo.filename = f'./szczepienia/csv/{date.strftime("szczepienia_%d.%m.%Y.csv")}'
        zipdata.extract(zipinfo)


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
async def covid(ctx):
    dateWEEKAgo = date - datetime.timedelta(weeks=1)
    dateYesterday = date - datetime.timedelta(days=1)
    with open(f'./covid/dane_powiat_{date.strftime("%d.%m.%Y")}.csv',
              'r') as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            if "Cały kraj" == row[1]:
                ilosc_zakazen = int(row[2])
                ilosc_zakazen_100k = round(float(row[3]) * 10, 1)
                ilosc_zgonow = int(row[4])
                ilosc_kwarantanna = int(row[9])
                ilosc_testow = int(row[10])
                ilosc_pozytywnych_testow = round(int(row[2]) / int(row[10]) * 100, 1)

    with open(
            f'./covid/dane_powiat_{dateWEEKAgo.strftime("%d.%m.%Y")}.csv',
            'r') as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            if "Cały kraj" == row[1]:
                ilosc_zakazen_WA = int(row[2])
                ilosc_zgonow_WA = int(row[4])

    with open(
            f'./covid/dane_powiat_{dateYesterday.strftime("%d.%m.%Y")}.csv',
            'r') as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            if "Cały kraj" == row[1]:
                ilosc_kwarantanna_Wczoraj = int(row[9])

    with open(
            f'./szczepienia/csv/szczepienia_{date.strftime("%d.%m.%Y")}.csv',
            'r') as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            if "liczba_szczepien_ogolem" != row[0]:
                ilosc_szczepien_dzis = int(row[1])
                ilosc_w_pelni_zaszczepionych = round(int(row[17]) / 38151000 * 100, 1)

    if ilosc_zakazen > ilosc_zakazen_WA:
        zmianaZK = f'o **{round((ilosc_zakazen / ilosc_zakazen_WA - 1) * 100)}%** więcej niż tydzień temu'
    elif ilosc_zakazen == ilosc_zakazen_WA:
        zmianaZK = f'Bez zmian(tyle samo co tydzień temu)'
    else:
        zmianaZK = f'o **{round((ilosc_zakazen_WA / ilosc_zakazen - 1) * 100)}%** mniej niż tydzień temu'

    if ilosc_zgonow > ilosc_zgonow_WA:
        zmianaZG = f'o **{round((ilosc_zgonow / ilosc_zgonow_WA - 1) * 100)}%** więcej niż tydzień temu'
    elif ilosc_zakazen == ilosc_zakazen_WA:
        zmianaZG = f'Bez zmian(tyle samo co tydzień temu)'
    else:
        zmianaZG = f'o **{round((ilosc_zgonow_WA / ilosc_zgonow - 1) * 100)}%** mniej niż tydzień temu'

    if ilosc_kwarantanna > ilosc_kwarantanna_Wczoraj:
        zmianaKW = f'o **{ilosc_kwarantanna - ilosc_kwarantanna_Wczoraj}** więcej niż wczoraj'
    elif ilosc_kwarantanna == ilosc_kwarantanna_Wczoraj:
        zmianaKW = f'Bez zmian(tyle samo co wczoraj)'
    else:
        zmianaKW = f'o **{(ilosc_kwarantanna - ilosc_kwarantanna_Wczoraj) * -1}** mniej niż wczoraj'

    embedColor = ""
    match (ilosc_zakazen_100k):
        case ilosc_zakazen_100k if ilosc_zakazen_100k <= 2:
            embedColor = 0xadd8e6
        case ilosc_zakazen_100k if 2 < ilosc_zakazen_100k <= 10:
            embedColor = 0x00c400
        case ilosc_zakazen_100k if 10 < ilosc_zakazen_100k <= 25:
            embedColor = 0xffff00
        case ilosc_zakazen_100k if 25 < ilosc_zakazen_100k <= 50:
            embedColor = 0xff3333
        case ilosc_zakazen_100k if 50 < ilosc_zakazen_100k <= 70:
            embedColor = 0x9a009a
        case ilosc_zakazen_100k if 70 < ilosc_zakazen_100k:
            embedColor = 0x292929

    embed = discord.Embed(
        title="COVID-19",
        description="Dzisiejsze statystyki COVID-19 z Ministerstwa Zdrowia",
        color=embedColor
    )
    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1069885833656844290/Inl2pghx_400x400.jpg")
    embed.add_field(name=f'Mamy {ilosc_zakazen} nowych zakażeń :microbe:', value=f'Jest to {zmianaZK}', inline=False)
    embed.add_field(name=f'Mamy {ilosc_zgonow} nowych zgonów :skull:', value=f'Jest to {zmianaZG}', inline=False)
    embed.add_field(name=f'Wykonano {ilosc_testow} testów :bar_chart:',
                    value=f'W tym **{ilosc_pozytywnych_testow}%** jest pozytywnych', inline=False)
    embed.add_field(name=f'Mamy {ilosc_kwarantanna} osób na kwarantannie :mask:', value=f'Jest to {zmianaKW}',
                    inline=False)
    embed.add_field(name=f'Wykonano {ilosc_szczepien_dzis} szczepień :syringe:',
                    value=f'W pełni zaszczepionych jest **{ilosc_w_pelni_zaszczepionych}%** Polaków', inline=False)

    await ctx.send(embed=embed)


bot.run(token)
