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

client = MyClient()
client.run(TOKEN)
