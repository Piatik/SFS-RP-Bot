import os
import discord
import datetime as dt

TOKEN = os.environ.get('DISCORD_TOKEN')

prefix = "&"
money=20

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.content.startswith(prefix + "ping"):
            await message.reply("Pong")
        if message.content.startswith(prefix + "say"):
            msg = message.content.replace(prefix + "say ", "") 
            embed=discord.Embed(title=message.author.name, color=0x00ffff, timestamp=dt.datetime.now())
            embed.add_field(name="Annonce", value=msg, inline=True)
            message.reply(embed=embed)
            await message.delete()

client = MyClient()
client.run(TOKEN)
