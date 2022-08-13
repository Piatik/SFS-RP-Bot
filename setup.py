import os
import discord
import datetime

TOKEN = os.environ.get('DISCORD_TOKEN')

prefix = "&"
money=20

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.content.startswith(prefix + "ping"):
            await message.reply("Pong")
        if message.content.startswith(prefix + "time"):
            embed=discord.Embed(title=message.author.name, color=0x00ffff, timestamp=datetime.datetime.now())
            await message.reply(embed=embed)

client = MyClient()
client.run(TOKEN)
