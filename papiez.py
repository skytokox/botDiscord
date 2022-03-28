import asyncio
import datetime
import discord
from discord.ext import commands, tasks

class papiez(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.ping2137.start()




    @tasks.loop(hours=24)
    async def ping2137(self):
        target_channel = 335070356941438977
        message_channel = self.bot.get_channel(target_channel)
        await asyncio.sleep(round(self.bot.latency * 10) + 0.6)
        await message_channel.send('<@&793218650563018794>')


    @ping2137.before_loop
    async def before_my_task(self):
        await self.bot.wait_until_ready()
        hour = 19
        minute = 37
        seconds = 0
        now = datetime.datetime.now()
        future = datetime.datetime(now.year, now.month, now.day, hour, minute, seconds)
        print((future - now).seconds)
        if now.hour >= hour and now.minute > minute:
            future += datetime.timedelta(days=1)
        await asyncio.sleep((future - now).seconds)

def setup(bot):
    bot.add_cog(papiez(bot))


