import asyncio
import csv
import datetime
import json
import random
import re
from urllib import request
from urllib.request import urlopen
from zipfile import ZipFile

import discord
from bs4 import BeautifulSoup
from discord.ext import commands, tasks


class OmicronData(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.omicronUpdate.start()

    @tasks.loop(hours=24)
    async def omicronUpdate(self):
        target_channel = 868423228853456966
        message_channel = self.bot.get_channel(target_channel)
        date = datetime.datetime.today()
        date_str = date.strftime("_%d.%m.%Y")
        url = "https://mendel3.bii.a-star.edu.sg/METHODS/corona/gamma/MUTATIONS/data/countryCount_b11529.json"
        color = [int(random.random() * 255), int(random.random() * 255), int(random.random() * 255)]
        omCountTEXT = ""

        with urlopen(url) as online:
            onlineData = json.load(online)
            for countries in onlineData:
                if countries['country'] == 'Poland':
                    totalOmicronOnline = countries['total']
                    shareOfOmicronOnline = countries['percvui_last4wks']
                    print(countries)
        try:
            with open(f'./omicron/omicron{date_str}.json', mode='r') as file:
                data = json.load(file)
                for countries in data:
                    if countries['country'] == 'Poland':
                        totalOmicron = countries['total']
                        shareOfOmicron = countries['percvui_last4wks']
                        print(countries)
        except:
            request.urlretrieve(url, f'./omicron/omicron{date_str}.json')
            totalOmicron = totalOmicronOnline
            shareOfOmicron = shareOfOmicronOnline

        if totalOmicronOnline != totalOmicron:
            print(f'nowy omikron!!!!{totalOmicronOnline - totalOmicron}')
            request.urlretrieve(url, f'./omicron/omicron{date_str}.json')
            newOmicronCases = totalOmicronOnline - totalOmicron
            totalOmicron = totalOmicronOnline
            shareOfOmicron = shareOfOmicronOnline

            match newOmicronCases:
                case 1:
                    omCountTEXT = " nowe zakażenie"
                case newOmicronCases if 2 <= newOmicronCases <= 4:
                    omCountTEXT = " nowe zakażenia"
                case newOmicronCases if 5 <= newOmicronCases:
                    omCountTEXT = " nowych zakażeń"

            embed = discord.Embed(
                title=f'Wykryto {newOmicronCases}{omCountTEXT} wariantem Omikron!<:microbe_2:921081559220629534>',
                description=f'Całkowita liczba przypadków Omikron to: {totalOmicron} \n Omikron to {shareOfOmicron}% sekwencji',
                color=discord.Color.from_rgb(color[0], color[1], color[2])
            )

            embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1069885833656844290/Inl2pghx_400x400.jpg")
            await message_channel.send(embed=embed)


    @omicronUpdate.before_loop
    async def before_my_task(self):
        await self.bot.wait_until_ready()
        hour = 11
        minute = 0
        seconds = 0
        now = datetime.datetime.now()
        future = datetime.datetime(now.year, now.month, now.day, hour, minute, seconds)
        print((future - now).seconds)
        if now.hour >= hour and now.minute > minute:
            future += datetime.timedelta(days=1)
        await asyncio.sleep((future - now).seconds)

    @commands.command()
    async def omicron(self, ctx):
        color = [int(random.random() * 255), int(random.random() * 255), int(random.random() * 255)]
        date = datetime.datetime.today()
        date_str = date.strftime("_%d.%m.%Y")
        dateYesterday = date - datetime.timedelta(days=1)
        dateYesterday_str = dateYesterday.strftime("_%d.%m.%Y")

        with open(f'./omicron/omicron{dateYesterday_str}.json', mode='r') as file:
            data = json.load(file)
            for countries in data:
                if countries['country'] == 'Poland':
                    totalOmicronYesterday = countries['total']
        with open(f'./omicron/omicron{date_str}.json', mode='r') as file:
            data = json.load(file)
            for countries in data:
                if countries['country'] == 'Poland':
                    totalOmicron = countries['total']
                    shareOfOmicron = countries['percvui_last4wks']

        newOmicronCases = totalOmicron - totalOmicronYesterday
        if newOmicronCases == 0:
            zmianaOM = ":arrow_right: Jest to **tyle samo** co wczoraj"
        else:
            zmianaOM = f':arrow_up: Jest to o **{newOmicronCases}** więcej niż wczoraj'

        embed = discord.Embed(
            title=f'Mamy {totalOmicron} zakażeń wariantem omikron <:microbe_2:921081559220629534>',
            description=f'{zmianaOM} \n\n :warning: Omikron to {shareOfOmicron}% sekwencji',
            color=discord.Color.from_rgb(color[0], color[1], color[2])
        )

        await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(OmicronData(bot))
