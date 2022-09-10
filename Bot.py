import os
import discord
import Cogs.Missions.Planete as Planete
from Cogs.Missions.Mission import Mission

TOKEN = os.environ.get('DISCORD_TOKEN')

bot = discord.Bot(debug_guilds=[988710399685840926])

@bot.event
async def on_ready():
    print('Logged on as {0}!'.format(bot.user))

    
bot.load_extension('Cogs.Missions.CogMission')
bot.load_extension('Cogs.CogHelp')
bot.run(TOKEN)
