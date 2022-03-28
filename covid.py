import asyncio
import csv
import datetime
import json
from urllib import request
from zipfile import ZipFile
import discord
from discord.ext import commands, tasks
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class CovidData(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.covidUpdate.start()

    @tasks.loop(hours=24)
    async def covidUpdate(self, send="True"):

        img = Image.open('./other/background.png')
        daysSinceStart = (datetime.date.today() - datetime.date(2020, 3, 4)).days
        date = datetime.datetime.today()
        date_str = date.strftime("_%d.%m.%Y")
        dateWEEKAgo = date - datetime.timedelta(weeks=1)
        dateYesterday = date - datetime.timedelta(days=1)
        target_channel = 868423228853456966
        message_channel = self.bot.get_channel(target_channel)

        urlCOVID = "https://www.arcgis.com/sharing/rest/content/items/6ff45d6b5b224632a672e764e04e8394/data"
        urlVACCINES = "https://www.arcgis.com/sharing/rest/content/items/3f47db945aff47e582db8aa383ccf3a1/data"

        local_file_COVID = f'dane_powiat{date_str}.csv'
        local_file_VACCINES = f'szczepienia{date_str}.zip'
        request.urlretrieve(urlCOVID, f'./covid/{local_file_COVID}')
        request.urlretrieve(urlVACCINES, f'./szczepienia/zip/{local_file_VACCINES}')

        zipdata = ZipFile(date.strftime('./szczepienia/zip/szczepienia_%d.%m.%Y.zip'), 'r')
        zipinfos = zipdata.infolist()
        for zipinfo in zipinfos:
            if 'rap_rcb_global_szczepienia.csv' in zipinfo.filename:
                zipinfo.filename = f'./szczepienia/csv/{date.strftime("szczepienia_%d.%m.%Y.csv")}'
                zipdata.extract(zipinfo)

        with open(f'./covid/dane_powiat_{date.strftime("%d.%m.%Y")}.csv',
                  mode='r', encoding="windows-1250") as file:
            reader = csv.reader(file, delimiter=";")
            for row in reader:
                if "Cały kraj" == row[1]:
                    cases_count = int(row[4])
                    deaths_count = int(row[8])
                    people_on_quarantine = int(row[13])
                    tests_count = int(row[14])
                    tests_positivity_rate = round(int(row[4]) / int(row[14]) * 100, 1)

        with open(
                f'./covid/dane_powiat_{dateWEEKAgo.strftime("%d.%m.%Y")}.csv',
                'r', encoding="windows-1250") as file:
            reader = csv.reader(file, delimiter=";")
            for row in reader:
                if dateWEEKAgo > datetime.datetime(2022, 2, 8):
                    if "Cały kraj" == row[1]:
                        cases_count_WA = int(row[4])
                        deaths_count_WA = int(row[8])
                else:
                    if "Cały kraj" == row[1]:
                        cases_count_WA = int(row[2])
                        deaths_count_WA = int(row[4])
        with open(
                f'./covid/dane_powiat_{dateYesterday.strftime("%d.%m.%Y")}.csv',
                'r', encoding="windows-1250") as file:
            reader = csv.reader(file, delimiter=";")
            for row in reader:
                if "Cały kraj" == row[1]:
                    people_on_quarantine_yesterday = int(row[13])
                    cases_count_yesterday = int(row[4])

        with open(
                f'./szczepienia/csv/szczepienia_{date.strftime("%d.%m.%Y")}.csv',
                'r', encoding="windows-1250") as file:
            reader = csv.reader(file, delimiter=";")
            for row in reader:
                if "liczba_szczepien_ogolem" != row[0]:
                    vaccinations_today = int(row[1])
                    people_with_2_doses = round(int(row[17]) / 38151000 * 100, 1)

        if cases_count > cases_count_WA:
            change_in_cases = f'Jest to o \n{round((cases_count / cases_count_WA - 1) * 100)}% więcej niż\ntydzień temu\n({cases_count_WA})'
        elif cases_count == cases_count_WA:
            change_in_cases = f'Bez zmian(tyle samo co tydzień temu)'
        else:
            change_in_cases = f'Jest to o \n{round((cases_count / cases_count_WA - 1) * 100) * -1}% mniej niż\ntydzień temu\n({cases_count_WA})'

        if deaths_count > deaths_count_WA:
            change_in_deaths = f'Jest to o \n{round((deaths_count / deaths_count_WA - 1) * 100)}% więcej niż \ntydzień temu\n({deaths_count_WA})'
        elif deaths_count == deaths_count_WA:
            change_in_deaths = f'Bez zmian(tyle samo co tydzień temu)'
        else:
            change_in_deaths = f'Jest to o \n{round((deaths_count_WA / deaths_count - 1) * 100)}% mniej niż \ntydzień temu\n({deaths_count_WA})'

        if people_on_quarantine > people_on_quarantine_yesterday:
            change_in_quarantine = f'Jest to o {people_on_quarantine - people_on_quarantine_yesterday}\nwięcej niż wczoraj'
        elif people_on_quarantine == people_on_quarantine_yesterday:
            change_in_quarantine = f'Bez zmian(tyle samo co wczoraj)'
        else:
            change_in_quarantine = f'Jest to o {(people_on_quarantine - people_on_quarantine_yesterday) * -1}\nmniej niż wczoraj'

        def dateToday():
            today = datetime.date.today()

            weekday = [u"Poniedziałek", u"Wtorek", u"Środa", u"Czwartek", u"Piątek", u"Sobota", u"Niedziela"]
            month = [u"Stycznia", u"Lutego", u"Marca", u"Kwietnia", u"Maja", u"Czerwca", u"Lipca", u"Sierpnia",
                     u"Września", u"Października", u"Listopada", u"Grudnia"]
            return f'{weekday[today.weekday()]} {today.day} {month[today.month - 1]} {today.year}'

        stats = ImageDraw.Draw(img)
        stats.line((250, 500) + (250, 1000), fill=(255, 255, 255))
        stats.line((650, 500) + (650, 1000), fill=(255, 255, 255))
        stats.line((1050, 500) + (1050, 1000), fill=(255, 255, 255))
        stats.line((1450, 500) + (1450, 1000), fill=(255, 255, 255))
        stats.line((1850, 500) + (1850, 1000), fill=(255, 255, 255))
        stats.line((2250, 500) + (2250, 1000), fill=(255, 255, 255))
        p1_font = ImageFont.truetype("./other/Lato-Bold.ttf", size=96)
        p2_font = ImageFont.truetype("./other/Lato-Bold.ttf", size=72)
        p3_font = ImageFont.truetype("./other/Lato-Bold.ttf", size=48)
        p4_font = ImageFont.truetype("./other/Lato-Bold.ttf", size=32)

        p1 = stats.textlength(text=f'{dateToday()}', font=p1_font)
        p1_position = (2500 - p1) / 2
        p2 = stats.textlength(text=f'{daysSinceStart} 'u"dzień pandemii COVID-19 w Polsce", font=p2_font)
        p2_position = (2500 - p2) / 2
        p3 = stats.textlength(text=u"Ilość zakażeń", font=p3_font)
        p3_position = (400 - p3) / 2 + 250
        p4 = stats.textlength(text=u"Jest to o 2137%", font=p4_font)
        p4_position = (400 - p4) / 2 + 250
        p5 = stats.textlength(text=u"Ilość śmierci", font=p3_font)
        p5_position = (400 - p5) / 2 + 650
        p6 = stats.textlength(text=u"Jest to wzrost o", font=p4_font)
        p6_position = (400 - p6) / 2 + 650
        p7 = stats.textlength(text=u"Ilość szczepień", font=p3_font)
        p7_position = (400 - p7) / 2 + 1050
        p8 = stats.textlength(text=u"W pełni zaszczepionych", font=p4_font)
        p8_position = (400 - p8) / 2 + 1050
        p9 = stats.textlength(text=u"kwarantannie", font=p3_font)
        p9_position = (400 - p9) / 2 + 1450
        p10 = stats.textlength(text=u"Jest to wzrost o", font=p4_font)
        p10_position = (400 - p10) / 2 + 1450
        p11 = stats.textlength(text=u"Ilość zrobionych", font=p3_font)
        p11_position = (400 - p11) / 2 + 1850
        p12 = stats.textlength(text=u"jest pozytywnych", font=p4_font)
        p12_position = (400 - p12) / 2 + 1850

        stats.text((p1_position, 25), f'{dateToday()}', fill=(255, 255, 255), font=p1_font)
        stats.text((p2_position, 187), f'{daysSinceStart} 'u"dzień pandemii COVID-19 w Polsce", fill=(255, 255, 255),
                   font=p2_font)
        stats.multiline_text((p3_position, 527), text=f'Ilość zakażeń\n\n\n{cases_count}', font=p3_font,
                             fill=(255, 255, 255),
                             align="center")
        stats.multiline_text((p4_position, 827), change_in_cases, fill=(255, 255, 255), font=p4_font,
                             align="center")
        stats.multiline_text((p5_position, 527), text=f'Ilość śmierci\n\n\n{deaths_count}', font=p3_font,
                             fill=(255, 255, 255),
                             align="center")
        stats.multiline_text((p6_position, 827), change_in_deaths, fill=(255, 255, 255), font=p4_font,
                             align="center")
        stats.multiline_text((p7_position, 527), text=f'Ilość szczepień\n\n\n{vaccinations_today}', font=p3_font,
                             fill=(255, 255, 255),
                             align="center")
        stats.multiline_text((p8_position, 827),
                             f'W pełni zaszczepionych\n jest {people_with_2_doses}% Polaków',
                             fill=(255, 255, 255),
                             font=p4_font, align="center")
        stats.multiline_text((p9_position, 527), text=f'Ilość osób na\n kwarantannie\n\n{people_on_quarantine}',
                             font=p3_font,
                             fill=(255, 255, 255), align="center")
        stats.multiline_text((p10_position, 827), change_in_quarantine, fill=(255, 255, 255), font=p4_font,
                             align="center")
        stats.multiline_text((p11_position, 527), text=f'Ilość zrobionych\ntestów\n\n{tests_count}', font=p3_font,
                             fill=(255, 255, 255), align="center")
        stats.multiline_text((p12_position, 827), f'w tym {tests_positivity_rate}% jest\npozytywnych',
                             fill=(255, 255, 255), font=p4_font,
                             align="center")

        img.save(f'./covid_stats_img/Statystyki{date_str}.png')
        print("Stworzono raport!")
        if cases_count != cases_count_yesterday:
            if send == "True":
                await message_channel.send(file=discord.File(f'./covid_stats_img/Statystyki{date_str}.png'))
        else:
            await asyncio.sleep(15)
            await self.covidUpdate()

    @covidUpdate.before_loop
    async def before_my_task(self):
        await self.bot.wait_until_ready()
        hour = 8
        minute = 30
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
        date_str = date.strftime("_%d.%m.%Y")
        dateYesterday = date - datetime.timedelta(days=1)
        dateYesterday_str = dateYesterday.strftime("_%d.%m.%Y")
        try:
            with open(f'./covid_stats_img/Statystyki{date_str}.png', mode='rb') as file:
                img_stats = discord.File(file)
                await ctx.send(file=img_stats)
        except:
            with open(f'./covid_stats_img/Statystyki{dateYesterday_str}.png', mode='rb') as file:
                img_stats = discord.File(file)
                await ctx.send(file=img_stats)

    @commands.command()
    async def create_file(self, ctx):
        await self.covidUpdate(send="False")
    # @commands.command()
    # async def wojewodztwa(self, ctx):
    #     date = datetime.datetime.now()
    #     date_str = date.strftime("_%d.%m.%Y")
    #     dateWA = date - datetime.timedelta(weeks=1)
    #     dateWA_str = dateWA.strftime("_%d.%m.%Y")
    #
    #     def voidvodshipsName(voidvodship):
    #         match (voidvodship):
    #             case 'Cały kraj':
    #                 return "W całym kraju"
    #             case 'mazowieckie':
    #                 return "W mazowieckim"
    #             case 'małopolskie':
    #                 return "W małopolskim"
    #             case 'śląskie':
    #                 return "W śląskim"
    #             case 'dolnośląskie':
    #                 return "W dolnośląśkim"
    #             case 'wielkopolskie':
    #                 return "W wielkopolskim"
    #             case 'pomorskie':
    #                 return 'W pomorskim'
    #             case 'łódzkie':
    #                 return "W łódzkim"
    #             case 'świętokrzyskie':
    #                 return 'W świętokrzyskim'
    #             case 'zachodniopomorskie':
    #                 return "W zachodniopomorskim"
    #             case 'podkarpackie':
    #                 return "W podkarpackim"
    #             case 'lubelskie':
    #                 return "W lubelskim"
    #             case 'lubuskie':
    #                 return "W lubuskim"
    #             case 'podlaskie':
    #                 return "W podlaskim"
    #             case 'kujawsko-pomorskie':
    #                 return "W kujawsko-pomorskim"
    #             case 'opolskie':
    #                 return "W opolskim"
    #             case 'warmińsko-mazurskie':
    #                 return "W warmińsko-mazurskim"
    #             case 'W całym kraju':
    #                 return "W całym kraju"
    #
    #     urlVoidvodships = "https://www.arcgis.com/sharing/rest/content/items/153a138859bb4c418156642b5b74925b/data"
    #     local_file_COVID = f'covid_voidvodships/dane_wojewodztwa'
    #
    #     request.urlretrieve(urlVoidvodships, f'{local_file_COVID}{date_str}.csv')
    #
    #     with open(f'{local_file_COVID}{date_str}.csv', mode='r', encoding="windows-1250") as file:
    #         reader = csv.reader(file, delimiter=";")
    #         for row in reader:
    #             if row[0] == 'Cały kraj':
    #                 cases_count_100k = round(float(row[3]) * 10, 1)
    #
    #     embedColor = ""
    #     match (cases_count_100k):
    #         case cases_count_100k if cases_count_100k <= 2:
    #             embedColor = 0xadd8e6
    #         case cases_count_100k if 2 < cases_count_100k <= 10:
    #             embedColor = 0x00c400
    #         case cases_count_100k if 10 < cases_count_100k <= 25:
    #             embedColor = 0xffff00
    #         case cases_count_100k if 25 < cases_count_100k <= 50:
    #             embedColor = 0xff3333
    #         case cases_count_100k if 50 < cases_count_100k <= 70:
    #             embedColor = 0x9a009a
    #         case cases_count_100k if 70 < cases_count_100k:
    #             embedColor = 0x292929
    #
    #     embed = discord.Embed(
    #         title="COVID-19",
    #         description="Dzisiejsze statystyki COVID-19 z podziałem na województwa",
    #         color=embedColor
    #     )
    #     voidvodships = {}
    #     voidvodshipsWA = {}
    #     with open(f'{local_file_COVID}{date_str}.csv', mode='r', encoding="windows-1250") as file:
    #         reader = csv.reader(file, delimiter=";")
    #         for row in reader:
    #             if row[0] != 'wojewodztwo':
    #                 voidvodships[row[0]] = int(row[1])
    #
    #     with open(f'{local_file_COVID}{dateWA_str}.csv', mode='r', encoding="windows-1250") as file:
    #         reader = csv.reader(file, delimiter=";")
    #         for row in reader:
    #             if row[0] != 'wojewodztwo':
    #                 voidvodshipsWA[row[0]] = int(row[1])
    #
    #     print(voidvodships)
    #     print(voidvodships['mazowieckie'])
    #     voidvodships_sorted = sorted(voidvodships.items(), key=lambda item: item[1])
    #     voidvodships_sorted.reverse()
    #
    #     for voidvodship in voidvodships_sorted:
    #
    #         cases_count = voidvodships[f'{voidvodship[0]}']
    #         cases_count_WA = voidvodshipsWA[f'{voidvodship[0]}']
    #
    #         if cases_count > cases_count_WA:
    #             weekChange = f':arrow_up: Jest to o **{round((cases_count / cases_count_WA - 1) * 100)}%** więcej niż tydzień temu'
    #         elif cases_count == cases_count_WA:
    #             weekChange = f':arrow_right: Bez zmian(tyle samo co tydzień temu)'
    #         else:
    #             weekChange = f':arrow_down: Jest to o **{round((cases_count / cases_count_WA - 1) * 100) * -1}%** mniej niż tydzień temu'
    #
    #         embed.add_field(name=f'{voidvodshipsName(voidvodship[0])} mamy {voidvodship[1]} zakażeń',
    #                         value=f'jest to o {weekChange}', inline=False)
    #
    #     await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(CovidData(bot))
