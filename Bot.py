import os
import discord
import Cogs.Missions.Planete as Planete
from Cogs.Missions.Mission import Mission

TOKEN = os.environ.get('DISCORD_TOKEN')

bot = discord.Client(debug_guilds=[988710399685840926])

bot.load_extension('Cogs.Missions.CogMission')


@discord.slash_command(
    name="help",
    description="Affichage des commandes"
)
def help(ctx):
    embed = discord.Embed(color=0x00ff00)
    embed.set_thumbnail(url="https://www.crushpixel.com/big-static14/preview4/planet-space-with-stars-shiny-1674010.jpg")
    embed.add_field(name="/mission", value="Permets de calculer vos couts de mission ainsi que vos bénefices facilement !")
    embed.add_field(name="/satellite", value="Affiche les satellite de la planete spécifier ainsi que leur couts")
    embed.add_field(name="/planete",value="Donne la table des couts pour les objectif de mission pour la planete spécifié")
    ctx.send(embed=embed)

bot.run(TOKEN)
