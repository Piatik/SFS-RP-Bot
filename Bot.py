import os
import discord
import Cogs.Missions.Planete as Planete
from Cogs.Missions.Mission import Mission

TOKEN = os.environ.get('DISCORD_TOKEN')

bot = discord.Bot(debug_guilds=[988710399685840926])

extensions = ['Cogs.Missions.CogMission','Cogs.CogHelp']
for cog in extensions:
    bot.load_extension(cog)


bot.run(TOKEN)