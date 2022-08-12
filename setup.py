import os
from os.path import join, dirname
from dotenv import load_dotenv

import discord


dotenv_path = join(dirname(__file__), 'id.env')
load_dotenv(dotenv_path)

TOKEN = os.getenv('DISCORD_TOKEN')

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

client = MyClient()
client.run(TOKEN)
