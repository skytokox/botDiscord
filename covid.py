import asyncio
import csv
import datetime
import re
from urllib import request
from urllib.request import urlopen
from zipfile import ZipFile

import discord
from bs4 import BeautifulSoup
from discord.ext import commands, tasks


class CovidData(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.covidUpdate.start()


    @tasks.loop(hours=24)
    async def covidUpdate(self):

        date = datetime.datetime.today()
        date_str = date.strftime("_%d.%m.%Y")
        target_channel = 868423228853456966
        message_channel = self.bot.get_channel(target_channel)

        urlCOVID = "https://www.arcgis.com/sharing/rest/content/items/6ff45d6b5b224632a672e764e04e8394/data"
        urlVACCINES = "https://www.arcgis.com/sharing/rest/content/items/3f47db945aff47e582db8aa383ccf3a1/data"
        urlVARIANTS = "https://newsnodes.com/omicron_tracker#"

        local_file_COVID = f'dane_powiat{date_str}.csv'
        local_file_VACCINES = f'szczepienia{date_str}.zip'
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

        dateWEEKAgo = date - datetime.timedelta(weeks=1)
        dateYesterday = date - datetime.timedelta(days=1)
        with open(f'./covid/dane_powiat_{date.strftime("%d.%m.%Y")}.csv',
                  'r') as file:
            reader = csv.reader(file, dialect="excel", delimiter=";")
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
            reader = csv.reader(file, dialect="excel", delimiter=";")
            for row in reader:
                if "Cały kraj" == row[1]:
                    ilosc_zakazen_WA = int(row[2])
                    ilosc_zgonow_WA = int(row[4])

        with open(
                f'./covid/dane_powiat_{dateYesterday.strftime("%d.%m.%Y")}.csv',
                'r') as file:
            reader = csv.reader(file, dialect="excel", delimiter=";")
            for row in reader:
                if "Cały kraj" == row[1]:
                    ilosc_kwarantanna_Wczoraj = int(row[9])

        with open(
                f'./szczepienia/csv/szczepienia_{date.strftime("%d.%m.%Y")}.csv',
                'r') as file:
            reader = csv.reader(file, dialect="excel", delimiter=";")
            for row in reader:
                if "liczba_szczepien_ogolem" != row[0]:
                    ilosc_szczepien_dzis = int(row[1])
                    ilosc_w_pelni_zaszczepionych = round(int(row[17]) / 38151000 * 100, 1)

        if ilosc_zakazen > ilosc_zakazen_WA:
            zmianaZK = f'o **{round((ilosc_zakazen / ilosc_zakazen_WA - 1) * 100)}%** więcej niż tydzień temu'
        elif ilosc_zakazen == ilosc_zakazen_WA:
            zmianaZK = f'Bez zmian(tyle samo co tydzień temu)'
        else:
            zmianaZK = f'o **{round((ilosc_zakazen / ilosc_zakazen_WA - 1) * 100) * -1}%** mniej niż tydzień temu'

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

        omCountTEXT = ""
        match totalOmicronCount:
            case 1:
                omCountTEXT = "zakażenie"
            case totalOmicronCount if 2 <= totalOmicronCount <= 4:
                omCountTEXT = "zakażenia"
            case totalOmicronCount if 5 <= totalOmicronCount:
                omCountTEXT = "zakażeń"
        if newOmicronCases == "":
            zmianaOM = "Jest to tyle samo co wczoraj"
        else:
            zmianaOM = f'o **{newOmicronCases}** więcej niż wczoraj'

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
        embed.add_field(name=f'Mamy {ilosc_zakazen} nowych zakażeń :microbe:', value=f'Jest to {zmianaZK}',
                        inline=False)
        embed.add_field(
            name=f'Mamy {totalOmicronCount} {omCountTEXT} wariantem omikron <:microbe_2:921081559220629534>',
            value=f'Jest to {zmianaOM}', inline=False)
        embed.add_field(name=f'Mamy {ilosc_zgonow} nowych zgonów :skull:', value=f'Jest to {zmianaZG}', inline=False)
        embed.add_field(name=f'Wykonano {ilosc_testow} testów :bar_chart:',
                        value=f'W tym **{ilosc_pozytywnych_testow}%** jest pozytywnych', inline=False)
        embed.add_field(name=f'Mamy {ilosc_kwarantanna} osób na kwarantannie :mask:', value=f'Jest to {zmianaKW}',
                        inline=False)
        embed.add_field(name=f'Wykonano {ilosc_szczepien_dzis} szczepień :syringe:',
                        value=f'W pełni zaszczepionych jest **{ilosc_w_pelni_zaszczepionych}%** Polaków', inline=False)

        await message_channel.send(embed=embed)

    @covidUpdate.before_loop
    async def before_my_task(self):
        await self.bot.wait_until_ready()
        hour = 23
        minute = 4
        seconds = 30
        now = datetime.datetime.now()
        future = datetime.datetime(now.year, now.month, now.day, hour, minute, seconds)
        print((future - now).seconds)
        if now.hour >= hour and now.minute > minute:
            future += datetime.timedelta(days=1)
        await asyncio.sleep((future - now).seconds)

    @commands.command()
    async def covid(self, ctx):
        date = datetime.datetime.today()
        dateWEEKAgo = date - datetime.timedelta(weeks=1)
        dateYesterday = date - datetime.timedelta(days=1)
        urlVARIANTS = "https://newsnodes.com/omicron_tracker#"

        page = urlopen(urlVARIANTS)
        soup = BeautifulSoup(page, 'html.parser')
        content = soup.find('img', {'src': "/images/flagsxs/PL.png"})
        content_parent = content.parent.parent
        totalOmicronCount = int(content_parent.find('td', {"class": "u-text-r"}).text)
        newOmicronCasesTXT = content_parent.find('span', {"style": "font-size: 9px"}).text
        newOmicronCases = int(re.search(r'\d+', newOmicronCasesTXT).group())

        with open(f'./covid/dane_powiat_{date.strftime("%d.%m.%Y")}.csv',
                  mode='r', encoding='ISO-8859-1') as file:
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
                'r',encoding='utf-8') as file:
            reader = csv.reader(file, dialect="excel", delimiter=";")
            for row in reader:
                if "Cały kraj" == row[1]:
                    ilosc_zakazen_WA = int(row[2])
                    ilosc_zgonow_WA = int(row[4])

        with open(
                f'./covid/dane_powiat_{dateYesterday.strftime("%d.%m.%Y")}.csv',
                'r', encoding='utf-8') as file:
            reader = csv.reader(file, dialect="excel", delimiter=";")
            for row in reader:
                if "Cały kraj" == row[1]:
                    ilosc_kwarantanna_Wczoraj = int(row[9])

        with open(
                f'./szczepienia/csv/szczepienia_{date.strftime("%d.%m.%Y")}.csv',
                'r', encoding='utf-8') as file:
            reader = csv.reader(file, dialect="excel", delimiter=";")
            for row in reader:
                if "liczba_szczepien_ogolem" != row[0]:
                    ilosc_szczepien_dzis = int(row[1])
                    ilosc_w_pelni_zaszczepionych = round(int(row[17]) / 38151000 * 100, 1)

        if ilosc_zakazen > ilosc_zakazen_WA:
            zmianaZK = f'o **{round((ilosc_zakazen / ilosc_zakazen_WA - 1) * 100)}%** więcej niż tydzień temu'
        elif ilosc_zakazen == ilosc_zakazen_WA:
            zmianaZK = f'Bez zmian(tyle samo co tydzień temu)'
        else:
            zmianaZK = f'o **{round((ilosc_zakazen / ilosc_zakazen_WA - 1) * 100) * -1}%** mniej niż tydzień temu'

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

        omCountTEXT = ""
        match totalOmicronCount:
            case 1:
                omCountTEXT = "zakażenie"
            case omicronCount if 2 <= omicronCount <= 4:
                omCountTEXT = "zakażenia"
            case omicronCount if 5 <= omicronCount:
                omCountTEXT = "zakażeń"
        if newOmicronCases == "":
            zmianaOM = "Jest to tyle samo co wczoraj"
        else:
            zmianaOM = f'o **{newOmicronCases}** więcej niż wczoraj'

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
        embed.add_field(name=f'Mamy {ilosc_zakazen} nowych zakażeń :microbe:', value=f'Jest to {zmianaZK}',
                        inline=False)
        embed.add_field(
            name=f'Mamy {totalOmicronCount} {omCountTEXT} wariantem omikron <:microbe_2:921081559220629534>',
            value=f'Jest to {zmianaOM}', inline=False)
        embed.add_field(name=f'Mamy {ilosc_zgonow} nowych zgonów :skull:', value=f'Jest to {zmianaZG}', inline=False)
        embed.add_field(name=f'Wykonano {ilosc_testow} testów :bar_chart:',
                        value=f'W tym **{ilosc_pozytywnych_testow}%** jest pozytywnych', inline=False)
        embed.add_field(name=f'Mamy {ilosc_kwarantanna} osób na kwarantannie :mask:', value=f'Jest to {zmianaKW}',
                        inline=False)
        embed.add_field(name=f'Wykonano {ilosc_szczepien_dzis} szczepień :syringe:',
                        value=f'W pełni zaszczepionych jest **{ilosc_w_pelni_zaszczepionych}%** Polaków', inline=False)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(CovidData(bot))
