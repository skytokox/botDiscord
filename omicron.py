import asyncio
import csv
import datetime
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



    @tasks.loop(minutes=5)
    async def omicronUpdate(self):
        date = datetime.datetime.now()
        date_str = date.strftime("_%d.%m.%Y")
        target_channel = 868423228853456966
        message_channel = self.bot.get_channel(target_channel)

        urlVARIANTS = "https://newsnodes.com/omicron_tracker#"
        page = urlopen(urlVARIANTS)
        soup = BeautifulSoup(page, 'html.parser')
        content = soup.find('img', {'src': "/images/flagsxs/PL.png"})
        content_parent = content.parent.parent
        totalOmicronCount = int(content_parent.find('td', {"class": "u-text-r"}).text)
        color = [int(random.random() * 255), int(random.random() * 255), int(random.random() * 255)]
        try:
            file = open(f'./omicron/omicron{date_str}.txt', 'r', encoding="windows-1250")
            lastUpdatedCount = int(re.findall(r'\d+', file.read())[3])
        except:
            lastUpdatedCount = totalOmicronCount
        if totalOmicronCount != lastUpdatedCount:
            newOmicronCases = totalOmicronCount - lastUpdatedCount
            lastUpdatedCount = totalOmicronCount
            omCountTEXT = ""
            match newOmicronCases:
                case 1:
                    omCountTEXT = " nowe zakażenie"
                case newOmicronCases if 2 <= newOmicronCases <= 4:
                    omCountTEXT = " nowe zakażenia"
                case newOmicronCases if 5 <= newOmicronCases:
                    omCountTEXT = " nowych zakażeń"
            embed = discord.Embed(
                title=f'Wykryto {newOmicronCases}{omCountTEXT} wariantem Omikron!<:microbe_2:921081559220629534>',
                description=f'Całkowita liczba przypadków Omikron to: {totalOmicronCount}',
                color=discord.Color.from_rgb(color[0], color[1], color[2])
            )
            embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1069885833656844290/Inl2pghx_400x400.jpg")
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
        minute = 45
        seconds = 0
        now = datetime.datetime.now()
        future = datetime.datetime(now.year, now.month, now.day, hour, minute, seconds)
        print((future - now).seconds)
        if now.hour >= hour and now.minute > minute:
            future += datetime.timedelta(days=1)
        await asyncio.sleep((future - now).seconds)

def setup(bot):
    bot.add_cog(OmicronData(bot))

