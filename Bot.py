import discord
import Cogs.Missions.Planete as Planete
from Cogs.Missions.Mission import Mission



bot = discord.Bot(debug_guilds=[988710399685840926])

extensions = ['Cogs.Missions.CogMission','Cogs.CogHelp']
for cog in extensions:
    bot.load_extension(cog)


bot.run('OTg4ODEwOTQwMjEwMzgwODMw.G0svH6.o8By9XvqCP9RaK-673K-R96Zn77PXIuY0goRTI')
