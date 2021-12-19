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



class OmicronData(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.omicronUpdate.start()



    @tasks.loop(minutes=5)
    async def omicronUpdate(self):
        date = datetime.datetime.now()
        date_str = date.strftime("_%d.%m.%Y")
        target_channel = 820650672697507870
        message_channel = self.bot.get_channel(target_channel)

        urlVARIANTS = "https://newsnodes.com/omicron_tracker#"
        page = urlopen(urlVARIANTS)
        soup = BeautifulSoup(page, 'html.parser')
        content = soup.find('img', {'src': "/images/flagsxs/PL.png"})
        content_parent = content.parent.parent
        totalOmicronCount = int(content_parent.find('td', {"class": "u-text-r"}).text)
        try:
            file = open(f'./omicron/omicron{date_str}.txt', 'r', encoding="windows-1250")
            lastUpdatedCount = int(re.findall(r'\d+', file.read())[3])
        except:
            lastUpdatedCount = totalOmicronCount

        if totalOmicronCount != lastUpdatedCount:
            newOmicronCases = totalOmicronCount - lastUpdatedCount
            lastUpdatedCount = totalOmicronCount
            match newOmicronCases:
                case 1:
                    omCountTEXT = "zakażenie"
                case totalOmicronCount if 2 <= totalOmicronCount <= 4:
                    omCountTEXT = "zakażenia"
                case totalOmicronCount if 5 <= totalOmicronCount:
                    omCountTEXT = "zakażeń"
            embed = discord.Embed(
                title=f':bangbang:Wykryto {newOmicronCases} nowe {omCountTEXT} wariantem Omikron<:microbe_2:921081559220629534>:bangbang:',
                description=f'Całkowita liczba przypadków Omikron to: {totalOmicronCount}',
                color=discord.colour.Color.orange()
            )
            # embed.add_field(name="", value=f'Całkowita liczba przypadków Omikron to: {totalOmicronCount}', inline=False)
            await message_channel.send(embed=embed)
            file = open(f'./omicron/omicron{date_str}.txt', 'w', encoding="windows-1250")
            file.write(f'Liczba przypadków Omikrona na dzień {date_str} to: {lastUpdatedCount}')
            file.close()
            print(f'Nowy omikron![{totalOmicronCount}]')
        else:
            file = open(f'./omicron/omicron{date_str}.txt', 'w', encoding="windows-1250")
            file.write(f'Liczba przypadków Omikrona na dzień {date_str} to: {totalOmicronCount}')
            file.close()
            print(f'Tyle samo omikrona![{totalOmicronCount}]')
    @omicronUpdate.before_loop
    async def before_my_task(self):
        await self.bot.wait_until_ready()
        hour = 20
        minute = 3
        seconds = 30
        now = datetime.datetime.now()
        future = datetime.datetime(now.year, now.month, now.day, hour, minute, seconds)
        print((future - now).seconds)
        if now.hour >= hour and now.minute > minute:
            future += datetime.timedelta(days=1)
        await asyncio.sleep((future - now).seconds)

def setup(bot):
    bot.add_cog(OmicronData(bot))

