import discord
from discord.ext import commands



class CogHelp(commands.Cog): 

    
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="help",
        description="Affichage des commandes"
    )
    async def help(self,ctx):
        embed = discord.Embed(color=0x00ff00)
        embed.set_thumbnail(url="https://www.crushpixel.com/big-static14/preview4/planet-space-with-stars-shiny-1674010.jpg")
        embed.add_field(name="/mission", value="Permets de calculer vos couts de mission ainsi que vos bénefices facilement !",inline = False)
        embed.add_field(name="/satellite", value="Affiche les satellite de la planete spécifier ainsi que leur couts",inline = False)
        embed.add_field(name="/planete",value="Donne la table des couts pour les objectif de mission pour la planete spécifié",inline = False)
        await ctx.send(embed=embed)

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(CogHelp(bot))