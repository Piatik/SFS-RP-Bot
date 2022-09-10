import os
import discord
import Cogs.Other.Planete as Planete
from Cogs.Other.Mission import Mission

TOKEN = os.environ.get('DISCORD_TOKEN')

bot = discord.Bot(debug_guilds=[988710399685840926])

@bot.event
async def on_ready():
    print('Logged on as {0}!'.format(bot.user))

print("Start CogMission Loading")
bot.load_extension('Cogs.Other.CogMission')
print("End CogMission Loading")
bot.load_extension('Cogs.CogHelp')
bot.run(TOKEN)
