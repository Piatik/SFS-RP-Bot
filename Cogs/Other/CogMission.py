import discord
from discord.ext import commands
from discord.ui import Button , View
from discord.ui import Modal
import sqlite3
import os.path
from Cogs.Other.Mission import Mission

liens = {"Venus": "data:image/jpeg;base64,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",
         "Mars": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRfl9LvcQc9VfbX47b8R6JYMmmk_hTyoaMfw&usqp=CAU",
         "Mercure": "https://cdn.futura-sciences.com/buildsv6/images/largeoriginal/e/d/f/edf75f57d9_82666_mercureok.jpg",
         "Jupiter": "https://static.actu.fr/uploads/2019/06/AdobeStock_234150167-960x640.jpeg",
         "Saturne": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Saturn_during_Equinox.jpg/1200px-Saturn_during_Equinox.jpg",
         "Uranus": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Uranus2.jpg/640px-Uranus2.jpg",
         "Neptune": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Neptune.jpg/280px-Neptune.jpg",
         "Pluton": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Nh-pluto-in-true-color_2x.jpg/290px-Nh-pluto-in-true-color_2x.jpg"
}

try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "sqlite.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

except sqlite3.Error as error:
    print("Failed to read data from sqlite table", error)

def GetPrixPlanete(planete): # recuperation des datas des planetes

    if planete == "Terre":
        cur.execute("""
        select prix, suborbital_prix,orbite_basse_prix,orbite_haute_prix,retour_terre_prix,docking_prix,mission_habite_prix,place_sup_prix 
        from planete 
        where nom_planete = \'Terre\';
        """)
        
        return cur

    elif planete == "Pluton" or planete == "Autre":
        cur.execute("""
        select prix, orbite_prix,sonde_prix,rover_prix,retour_terre_prix,survol_prix 
        from planete
        where nom_planete = \'{}\';
        """.format(planete))
   
        return cur
    
    else :
        cur.execute("""
        select prix, orbite_prix,sonde_prix,rover_prix,retour_terre_prix,mission_habite_prix,place_sup_prix,survol_prix
        from planete 
        where nom_planete = \'{}\';
        """.format(planete))
    
        return cur



def GetPrixSatellite(planete):
    cur.execute("""SELECT satelite.satelite_nom, satelite.prix 
    from satelite, planete 
    where satelite.planete_id = planete.id 
    and planete.nom_planete = \'{}\';
    """.format(planete))

   
    return cur
#endregion

def getEmbed(embed,planete): # Methode de traitement de l'affichage

    data = GetPrixPlanete(planete) # recuperation des donées

    if planete == "Terre":

        embed.title="Table des prix pour **__la Terre__**"
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Earth_by_the_EPIC_Team_on_21_April_2018.png/280px-Earth_by_the_EPIC_Team_on_21_April_2018.png")
        embed.description="Les prix doivent **s'additionner** selon les besoins de la **mission**"
        for row in data:
            embed.add_field(name="Prix de la __mission__",value= "{}\n".format(convert(row[0])),inline=False )
            embed.add_field(name="Prix du vol __suborbital__ ",value= "{}\n".format(convert(row[1])),inline=False )
            embed.add_field(name="Prix du vol en __orbite basse__ ",value= "{}\n".format(convert(row[2])),inline=False )
            embed.add_field(name="Prix du vol en __orbite haute__",value= "{}\n".format(convert(row[3])),inline=False )
            embed.add_field(name="Prix du __retour sur terre__",value= "{}\n".format(convert(row[4])),inline=False )
            embed.add_field(name="Prix du __docking__",value= "{}\n".format(convert(row[5])),inline=False )
            embed.add_field(name="Prix du __vol habitee__",value= "{}\n".format(convert(row[6])),inline=False )
            embed.add_field(name="Prix d'une __place supplementaire__",value= "{}\n".format(convert(row[7])),inline=False )

        
    elif planete == "Pluton" or planete == "Autre":

        embed.title="Table des prix pour **__{}__**".format(planete)
        embed.description="Les prix doivent **s'additionner** selon les besoins de la **mission**"
        for row in data:
            embed.add_field(name="Prix de la __mission__",value= "{}\n".format(convert(row[0])),inline=False )
            embed.add_field(name="Prix du vol en __orbite__ ",value= "{}\n".format(convert(row[1])),inline=False )
            embed.add_field(name="Prix de la __sonde__ ",value= "{}\n".format(convert(row[2])),inline=False )
            embed.add_field(name="Prix du __rover__",value= "{}\n".format(convert(row[3])),inline=False )
            embed.add_field(name="Prix du __retour sur terre__",value= "{}\n".format(convert(row[4])),inline=False )
            embed.add_field(name="Prix du __survol__",value= "{}\n".format(convert(row[5])),inline=False )

        
    else:
        embed.title="Table des prix pour **__{}__**".format(planete)
        embed.description="Les prix doivent **s'additionner** selon les besoins de la **mission**"
        for row in data:
            embed.add_field(name="Prix de la __mission__",value= "{}\n".format(convert(row[0])),inline=False )
            embed.add_field(name="Prix du vol en __orbite__ ",value= "{}\n".format(convert(row[1])),inline=False )
            embed.add_field(name="Prix de la __sonde__ ",value= "{}\n".format(convert(row[2])),inline=False )
            embed.add_field(name="Prix du __rover__",value= "{}\n".format(convert(row[3])),inline=False )
            embed.add_field(name="Prix du __retour sur terre__",value= "{}\n".format(convert(row[4])),inline=False )
            embed.add_field(name="Prix du __vol habitee__",value= "{}\n".format(convert(row[5])),inline=False )
            embed.add_field(name="Prix d'une __place supplementaire__",value= "{}\n".format(convert(row[6])),inline=False )
            embed.add_field(name="Prix du __survol__",value= "{}\n".format(convert(row[7])),inline=False )

        
    return embed
def formatNomPlanete(planete):
    planete = str(planete).title()
    planete = planete.replace('é','e')
    planete = planete.replace('è','e')
    return planete
    
def convert(val):

    if val >= 1000000000:
        val = "{} Milliard".format(val/1000000000)
    elif val < 1000000000 : 
        val = "{} Million".format(val/1000000)
    return val


class MyModal(discord.ui.Modal):
    missionObj = None
    embedPrincipal = None
    def __init__(self,missionObj,embedPrincipal, *args, **kwargs) -> None:
        self.missionObj = missionObj
        self.embedPrincipal = embedPrincipal
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Nombre de places"))

    async def callback(self, interaction: discord.Interaction):
        self.missionObj.PlaceSup(self.children[0].value)
        embed = self.embedPrincipal
        embed.title="Récapitulatif de votre mission :"
        embed.add_field(name="Couts ", value="{}\n({})".format(convert(self.missionObj.GetPrix()), str(self.missionObj.GetPrix()) ))
        embed.add_field(name="Bénefices",value="{}\n({})".format(convert(self.missionObj.GetRecette()), str(self.missionObj.GetRecette())))
        await interaction.response.edit_message(embed=embed,view=None)
      


class CogMission(commands.Cog): 
   
    def __init__(self, bot):
        self.bot = bot
    
    @discord.slash_command(
        name="mission",
        description="calculez les couts et benefices de votre mission ici!",
    )
    async def mission(self,ctx,planete):  

        author = ctx.author
#region Code horrible a refactor si possible 
#------------------------------------------ Buttons -------------------------------------------

        buttonOui = Button(label="Oui",style=discord.ButtonStyle.primary)
        buttonNon = Button(label="Non",style=discord.ButtonStyle.danger)

        view=View()
        view.add_item(buttonOui)
        view.add_item(buttonNon)
#----------------------------------------------------------------------------------------------



#-------------------------------------------- Buttons Callback Extra-Terrestre ----------------------------------------------
        async def CButtonRoverOui(interaction):
            if interaction.user.id == author.id:
                missionObj.Rover()
                embed = embedPrincipal
                embed.clear_fields()
                buttonOui.callback = CButtonSondeOui
                buttonOui.callback = CButtonSondeNon
                embed.title="Y aura t'il une sonde ?"
                await interaction.response.edit_message(embed=embed,view=view)
            

        async def CButtonRoverNon(interaction):
            if interaction.user.id == author.id:
                embed = embedPrincipal
                embed.clear_fields()
                buttonOui.callback = CButtonSondeOui
                buttonNon.callback = CButtonSondeNon
                embed.title="Y aura t'il une sonde ?"
                await interaction.response.edit_message(embed=embed,view=view)


        async def CButtonSondeOui(interaction):
            if interaction.user.id == author.id:
                missionObj.Sonde()
                embed = embedPrincipal
                embed.clear_fields()
                buttonOui.callback = CButtonOrbiteOui
                buttonNon.callback = CButtonOrbiteNon
                embed.title="Le vol sera t'il en orbite ?"
                await interaction.response.edit_message(embed=embed,view=view)

        async def CButtonSondeNon(interaction):
            if interaction.user.id == author.id:
                embed = embedPrincipal
                embed.clear_fields()
                buttonOui.callback = CButtonOrbiteOui
                buttonNon.callback = CButtonOrbiteNon
                embed.title="Le vol sera t'il en orbite ?"
                await interaction.response.edit_message(embed=embed,view=view)


        async def CButtonOrbiteOui(interaction):
            if interaction.user.id == author.id:
                missionObj.Orbite()
                embed = embedPrincipal
                embed.clear_fields()
                buttonOui.callback = CButtonRetourOui
                buttonNon.callback = CButtonRetourNon
                embed.title="Un retour sur terre est-il prévu ?"
                await interaction.response.edit_message(embed=embed,view=view)

        async def CButtonOrbiteNon(interaction):
            if interaction.user.id == author.id:
                embed = embedPrincipal
                buttonOui.callback = CButtonRetourOui
                buttonNon.callback = CButtonRetourNon
                embed.title="Un retour sur terre est-il prévu ?"
                embed.clear_fields()
                await interaction.response.edit_message(embed=embed,view=view)


#-------------------------------------------- Buttons Callback Generaux ----------------------------------------------

        async def CButtonRetourOui(interaction):
            if interaction.user.id == author.id:
                missionObj.RetourTerre()
                embed = embedPrincipal
                embed.clear_fields()
                if missionObj.planete == "Autre":
                    embed.title="Récapitulatif de votre mission :"
                    embed.add_field(name="Couts ", value=str(missionObj.GetPrix()))
                    embed.add_field(name="Bénefices",value= str(missionObj.GetRecette()))
                    await interaction.response.edit_message(embed=embed,view=None)
                else :
                    buttonOui.callback = CButtonVolHabOui
                    buttonNon.callback = CButtonVolHabNon
                    embed.title="La mission sera t'elle habité ?"
                    await interaction.response.edit_message(embed=embed,view=view)

        async def CButtonRetourNon(interaction):
            if interaction.user.id == author.id:
                embed = embedPrincipal
                embed.clear_fields()
                if missionObj.planete == "Autre":
                    embed.title="Récapitulatif de votre mission :"
                    embed.add_field(name="Couts ", value=str(missionObj.GetPrix()))
                    embed.add_field(name="Bénefices",value= str(missionObj.GetRecette()))
                    await interaction.response.edit_message(embed=embed,view=None)    
                else :
                    buttonOui.callback = CButtonVolHabOui
                    buttonNon.callback = CButtonVolHabNon
                    embed.title="La mission sera t'elle habité ?"
                    await interaction.response.edit_message(embed=embed,view=view)


        async def CButtonVolHabOui(interaction):
            if interaction.user.id == author.id:
                missionObj.VolHabitee()
                buttonOui.callback = CButtonPlaceSupOui
                buttonNon.callback = CButtonPlaceSupNon
                embed = embedPrincipal
                embed.clear_fields()
                embed.title="Vous faut-il une place supplémentaire ?"
                await interaction.response.edit_message(embed = embed, view=view)

        async def CButtonVolHabNon(interaction):
            if interaction.user.id == author.id:
                embed = embedPrincipal
                embed.title="Récapitulatif de votre mission :"
                embed.clear_fields()
                embed.add_field(name="Couts ", value="{}\n({})".format(convert(missionObj.GetPrix()), str(missionObj.GetPrix()) ))
                embed.add_field(name="Bénefices",value="{}\n({})".format(convert(missionObj.GetRecette()), str(missionObj.GetRecette())))
                await interaction.response.edit_message(embed=embed,view=None)
        

        async def CButtonPlaceSupOui(interaction):
            if interaction.user.id == author.id:
                await interaction.response.send_modal(MyModal(title="Places supplémentaire",missionObj=missionObj,embedPrincipal = embedPrincipal))


        async def CButtonPlaceSupNon(interaction):
            if interaction.user.id == author.id:
                embed = embedPrincipal
                embed.title="Récapitulatif de votre mission :"
                embed.clear_fields()
                embed.add_field(name="Couts ", value="{}\n({})".format(convert(missionObj.GetPrix()), str(missionObj.GetPrix()) ))
                embed.add_field(name="Bénefices",value="{}\n({})".format(convert(missionObj.GetRecette()), str(missionObj.GetRecette())))
                await interaction.response.edit_message(embed=embed,view=None)

#-------------------------------------------- Buttons Callback Terrestre ----------------------------------------------
        async def CButtonOrbHOui(interaction):
            if interaction.user.id == author.id:
                missionObj.OrbiteHaute()
                buttonOui.callback = CButtonOrbBOui
                buttonNon.callback = CButtonOrbBNon

                embed = embedPrincipal
                embed.clear_fields()
                embed.title="La mission est prévu pour un Docking ?"
                await interaction.response.edit_message(embed=embed,view=view)

        async def CButtonOrbHNon(interaction):
            if interaction.user.id == author.id:
                buttonOui.callback = CButtonOrbBOui
                buttonNon.callback = CButtonOrbBNon
                embed = embedPrincipal
                embed.clear_fields()
                embed.title= "Le vol est il prévu pour etre en Orbite basse "
                await interaction.response.edit_message(embed=embed,view=view)
    


        async def CButtonOrbBOui(interaction):
            if interaction.user.id == author.id:
                missionObj.OrbiteBasse()
                buttonOui.callback = CButtonDockOui
                buttonNon.callback = CButtonDockNon
                embed = embedPrincipal
                embed.clear_fields()
                embed.title= "La mission est prévu pour un Docking ?"
                await interaction.response.edit_message(embed=embed,view=view)

        async def CButtonOrbBNon(interaction):
            if interaction.user.id == author.id:
                buttonOui.callback = CButtonDockOui
                buttonNon.callback = CButtonDockNon
                embed = embedPrincipal
                embed.clear_fields()
                embed.title="La mission est prévu pour un Docking ?"
                await interaction.response.edit_message(embed=embed,view=view)

        async def CButtonDockOui(interaction):
            if interaction.user.id == author.id:
                missionObj.Docking()
                embed = embedPrincipal
                if missionObj.altChoisie:
                    buttonOui.callback = CButtonRetourOui
                    buttonNon.callback = CButtonRetourNon
                    embed.clear_fields()
                    embed.title= "La mission est prévu pour un retour sur terre ?"
                    await interaction.response.edit_message(embed=embed,view=view)
                else:
                    buttonOui.callback = CButtonSubOui
                    buttonNon.callback = CButtonSubNon
                    embed.clear_fields()
                    embed.title= "La mission est prévu pour un vol suborbital ?"
                    await interaction.response.edit_message(embed=embed,view=view)


        async def CButtonDockNon(interaction):
            if interaction.user.id == author.id:
                embed = embedPrincipal
                if missionObj.altChoisie:
                    buttonOui.callback = CButtonRetourOui
                    buttonNon.callback = CButtonRetourNon
                    embed.clear_fields()
                    embed.title="La mission est prévu pour un retour sur terre ?"
                    await interaction.response.edit_message(embed=embed,view=view)
                else:
                    buttonOui.callback = CButtonSubOui
                    buttonNon.callback = CButtonSubNon
                    embed.clear_fields()
                    embed.title="La mission est prévu pour un vol suborbital ?"
                    await interaction.response.edit_message(embed=embed,view=view)
            

        async def CButtonSubOui(interaction):
            if interaction.user.id == author.id:
                missionObj.Suborbital()
                view=View()
                buttonOui.callback = CButtonRetourOui
                buttonNon.callback = CButtonRetourNon
                embed = embedPrincipal
                embed.clear_fields()
                embed.title="La mission est prévu pour un retour sur terre ?"
                await interaction.response.edit_message(embed=embed,view=view)
    
        async def CButtonSubNon(interaction):
            if interaction.user.id == author.id:
                buttonOui.callback = CButtonRetourOui
                buttonNon.callback = CButtonRetourNon
                embed = embedPrincipal
                embed.clear_fields()
                embed.title="La mission est prévu pour un retour sur terre ?"
                await interaction.response.edit_message(embed=embed,view=view)

#------------------------------------------------------------------------------------------------------------------------
#endregion 

        missionObj = Mission()

        embedPrincipal = discord.Embed(color=0x00ff00)

        planete = formatNomPlanete(planete)
    
    
        if planete in missionObj.nomPlanete :
            if planete == "Lune":
                embedPrincipal.set_author(name="Mission vers la Lune, satellite de la Terre par @{}".format(ctx.author.name))
                embedPrincipal.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Moon_nearside_LRO_5000_%282%29.png/330px-Moon_nearside_LRO_5000_%282%29.png")
            elif planete == "Autre":
                embedPrincipal.set_author(name="Mission vers une planete lointaine par @{}".format(ctx.author.name))
                embedPrincipal.set_thumbnail(url="https://www.crushpixel.com/big-static14/preview4/planet-space-with-stars-shiny-1674010.jpg")
            else :
                embedPrincipal.set_author(name="Mission vers {} par @{}".format(planete,ctx.author.name))
                embedPrincipal.set_thumbnail(url=liens[str(planete)])
            embed = embedPrincipal
            embed.clear_fields()
            missionObj.SetPlanete(planete)
        
            if(planete != "Terre"):
                buttonOui.callback = CButtonRoverOui
                buttonNon.callback = CButtonRoverNon
                embed.title = "Y aura t'il un rover ?"
                await ctx.respond(embed=embed, view=view)
            else :
                buttonOui.callback = CButtonOrbHOui
                buttonNon.callback = CButtonOrbHNon
                embed.title="Le vol est-il prevu pour une vol en orbite Haute ?"
                await ctx.respond(embed=embed, view=view)

        elif planete in missionObj.nomSat:
            missionObj.SetPlaneteBySat(planete)
            embedPrincipal.set_author(name="Mission vers {}, satellite de {} par @{}".format(missionObj.cible,missionObj.planete,ctx.author.name))
            embed = embedPrincipal 
            embed.clear_fields()

            if(missionObj.planete != "Terre"):
                buttonOui.callback = CButtonRoverOui
                buttonNon.callback = CButtonRoverNon
                embed.title = "Y aura t'il un rover ?"
                await ctx.respond(embed=embed, view=view)
            else :
                buttonOui.callback = CButtonOrbHOui
                buttonNon.callback = CButtonOrbHNon
                embed.title="Le vol est-il prevu pour une vol en orbite Haute ?"
                await ctx.respond(embed=embed, view=view)

        else :
            await ctx.respond(embed = discord.Embed(title = "Veuiller verifier l'orthogrape du nom de votre planete ou satellite",color = discord.Color.red))



    @discord.slash_command(
        name="prix",
        description="Affichage de la table des prix de la planete choisie",
    ) # fonction prenant en parametre le nom d'une planete et retourne toutes les info monetaire la concernant 
    async def prix(self,ctx, arg):
        missionObj = Mission()
        embedPrincipal = discord.Embed(color=0x00ff00)
        embedPrincipal.set_thumbnail(url="https://www.crushpixel.com/big-static14/preview4/planet-space-with-stars-shiny-1674010.jpg")

        arg = formatNomPlanete(arg)
    
        assert arg in missionObj.nomPlanete, await ctx.send(embed = discord.Embed(title = "Veuiller verifier l'orthogrape du nom de votre planete"))  # verif que la planete existe

        await ctx.respond(embed=getEmbed(embedPrincipal,arg))

    @discord.slash_command(
        name="satellite",
        description="Liste des satellites de la planete choisis et de leur prix",
    ) # Fonction permettant de renvoyer toutes les lunes d'une planete 
    async def satellite(self,ctx, arg):
        missionObj = Mission()
        embeded = discord.Embed(color=0x00ff00)
        embeded.set_thumbnail(url="https://www.crushpixel.com/big-static14/preview4/planet-space-with-stars-shiny-1674010.jpg")

        arg = formatNomPlanete(arg)
        assert arg in missionObj.nomPlanete, await ctx.send(embed = discord.Embed(title = "Veuiller verifier l'orthogrape du nom de votre planete !")) # verif que la planete existe
        assert arg in missionObj.nomPlaneteSat, await ctx.send(embed = discord.Embed(title = "Il n'y a pas de satellite pour cette Planete !")) # verif que la planete as un satellite
    
        cur = GetPrixSatellite(arg)
    
        embeded.title="Satellites de __{}__".format(arg)
    
        for row in cur:
       
            embeded.add_field(name="{}".format(row[0]), value="{}".format(convert(row[1])), inline=False)

        await ctx.respond(embed = embeded)


def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(CogMission(bot))
