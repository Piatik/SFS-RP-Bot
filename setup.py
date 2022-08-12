import os
import discord

TOKEN = os.environ.get('DISCORD_TOKEN')

prefix = "&"

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.content.startswith(prefix + "ping"):
            await message.reply("Pong")
        if message.content.startswith(prefix + "money"):
            embed=discord.Embed(title=name, color=0x00ffff)
            embed.add_field(name="Money" , value=money, inline=True)
            await message.send(embed=embed)

client = MyClient()
client.run(TOKEN)
