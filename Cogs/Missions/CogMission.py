from turtle import title
import discord
from discord.ext import commands
from discord.ui import Button , View
from interactions import Modal
from Cogs.Missions.Mission import Mission
import sqlite3
import os.path


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
    missionObj = NULL
    embedPrincipal = NULL
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
            missionObj.Rover()
            embed = embedPrincipal
            embed.clear_fields()
            buttonOui.callback = CButtonSondeOui
            buttonOui.callback = CButtonSondeNon
            embed.title="Y aura t'il une sonde ?"
            await interaction.response.edit_message(embed=embed,view=view)

        async def CButtonRoverNon(interaction):
            embed = embedPrincipal
            embed.clear_fields()
            buttonOui.callback = CButtonSondeOui
            buttonNon.callback = CButtonSondeNon
            embed.title="Y aura t'il une sonde ?"
            await interaction.response.edit_message(embed=embed,view=view)


        async def CButtonSondeOui(interaction):
            missionObj.Sonde()
            embed = embedPrincipal
            embed.clear_fields()
            buttonOui.callback = CButtonOrbiteOui
            buttonNon.callback = CButtonOrbiteNon
            embed.title="Le vol sera t'il en orbite ?"
            await interaction.response.edit_message(embed=embed,view=view)

        async def CButtonSondeNon(interaction):
            embed = embedPrincipal
            embed.clear_fields()
            buttonOui.callback = CButtonOrbiteOui
            buttonNon.callback = CButtonOrbiteNon
            embed.title="Le vol sera t'il en orbite ?"
            await interaction.response.edit_message(embed=embed,view=view)


        async def CButtonOrbiteOui(interaction):
            missionObj.Orbite()
            embed = embedPrincipal
            embed.clear_fields()
            buttonOui.callback = CButtonRetourOui
            buttonNon.callback = CButtonRetourNon
            embed.title="Un retour sur terre est-il prévu ?"
            await interaction.response.edit_message(embed=embed,view=view)

        async def CButtonOrbiteNon(interaction):
            embed = embedPrincipal
            buttonOui.callback = CButtonRetourOui
            buttonNon.callback = CButtonRetourNon
            embed.title="Un retour sur terre est-il prévu ?"
            embed.clear_fields()
            await interaction.response.edit_message(embed=embed,view=view)


#-------------------------------------------- Buttons Callback Generaux ----------------------------------------------

        async def CButtonRetourOui(interaction):
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
            missionObj.VolHabitee()
            buttonOui.callback = CButtonPlaceSupOui
            buttonNon.callback = CButtonPlaceSupNon
            embed = embedPrincipal
            embed.clear_fields()
            embed.title="Vous faut-il une place supplémentaire ?"
            await interaction.response.edit_message(embed = embed, view=view)

        async def CButtonVolHabNon(interaction):
            embed = embedPrincipal
            embed.title="Récapitulatif de votre mission :"
            embed.clear_fields()
            embed.add_field(name="Couts ", value="{}\n({})".format(convert(missionObj.GetPrix()), str(missionObj.GetPrix()) ))
            embed.add_field(name="Bénefices",value="{}\n({})".format(convert(missionObj.GetRecette()), str(missionObj.GetRecette())))
            await interaction.response.edit_message(embed=embed,view=None)
       

        async def CButtonPlaceSupOui(interaction):
            await interaction.response.send_modal(MyModal(title="Places supplémentaire",missionObj=missionObj,embedPrincipal = embedPrincipal))


        async def CButtonPlaceSupNon(interaction):
            embed = embedPrincipal
            embed.title="Récapitulatif de votre mission :"
            embed.clear_fields()
            embed.add_field(name="Couts ", value="{}\n({})".format(convert(missionObj.GetPrix()), str(missionObj.GetPrix()) ))
            embed.add_field(name="Bénefices",value="{}\n({})".format(convert(missionObj.GetRecette()), str(missionObj.GetRecette())))
            await interaction.response.edit_message(embed=embed,view=None)


#-------------------------------------------- Buttons Callback Terrestre ----------------------------------------------
        async def CButtonOrbHOui(interaction):
            missionObj.OrbiteHaute()
            buttonOui.callback = CButtonOrbBOui
            buttonNon.callback = CButtonOrbBNon

            embed = embedPrincipal
            embed.clear_fields()
            embed.title="La mission est prévu pour un Docking ?"
            await interaction.response.edit_message(embed=embed,view=view)

        async def CButtonOrbHNon(interaction):
            buttonOui.callback = CButtonOrbBOui
            buttonNon.callback = CButtonOrbBNon
            embed = embedPrincipal
            embed.clear_fields()
            embed.title= "Le vol est il prévu pour etre en Orbite basse "
            await interaction.response.edit_message(embed=embed,view=view)
   


        async def CButtonOrbBOui(interaction):
            missionObj.OrbiteBasse()
            buttonOui.callback = CButtonDockOui
            buttonNon.callback = CButtonDockNon
            embed = embedPrincipal
            embed.clear_fields()
            embed.title= "La mission est prévu pour un Docking ?"
            await interaction.response.edit_message(embed=embed,view=view)

        async def CButtonOrbBNon(interaction):
            buttonOui.callback = CButtonDockOui
            buttonNon.callback = CButtonDockNon
            embed = embedPrincipal
            embed.clear_fields()
            embed.title="La mission est prévu pour un Docking ?"
            await interaction.response.edit_message(embed=embed,view=view)

        async def CButtonDockOui(interaction):
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
            missionObj.Suborbital()
            view=View()
            buttonOui.callback = CButtonRetourOui
            buttonNon.callback = CButtonRetourNon
            embed = embedPrincipal
            embed.clear_fields()
            embed.title="La mission est prévu pour un retour sur terre ?"
            await interaction.response.edit_message(embed=embed,view=view)
    
        async def CButtonSubNon(interaction):
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
        embedPrincipal.set_thumbnail(url="https://www.crushpixel.com/big-static14/preview4/planet-space-with-stars-shiny-1674010.jpg")

        planete = formatNomPlanete(planete)
    
    
        if planete in missionObj.nomPlanete :
        
            embedPrincipal.set_author(name="Mission vers {} par @{}".format(planete,ctx.author.name))
            embed = embedPrincipal
            embed.clear_fields()
            missionObj.SetPlanete(planete)
        
            if(planete != "Terre"):
                buttonOui.callback = CButtonRoverOui
                buttonNon.callback = CButtonRoverNon
                embed.title = "Y aura t'il un rover ?"
                await ctx.send(embed=embed, view=view)
            else :
                buttonOui.callback = CButtonOrbHOui
                buttonNon.callback = CButtonOrbHNon
                embed.title="Le vol est-il prevu pour une vol en orbite Haute ?"
                await ctx.send(embed=embed, view=view)

        elif planete in missionObj.nomSat:
            missionObj.SetPlaneteBySat(planete)
            embedPrincipal.set_author(name="Mission vers {}, satellite de {} par @{}".format(missionObj.cible,missionObj.planete,ctx.author.name))
            embed = embedPrincipal 
            embed.clear_fields()

            if(missionObj.planete != "Terre"):
                buttonOui.callback = CButtonRoverOui
                buttonNon.callback = CButtonRoverNon
                embed.title = "Y aura t'il un rover ?"
                await ctx.send(embed=embed, view=view)
            else :
                buttonOui.callback = CButtonOrbHOui
                buttonNon.callback = CButtonOrbHNon
                embed.title="Le vol est-il prevu pour une vol en orbite Haute ?"
                await ctx.send(embed=embed, view=view)

        else :
            await ctx.send(embed = discord.Embed(title = "Veuiller verifier l'orthogrape du nom de votre planete ou satellite",color = discord.Color.red))



    @discord.slash_command(
        name="prix",
        description="Affichage de la table des prix de la planete choisie",
    ) # fonction prenant en parametre le nom d'une planete et retourne toutes les info monetaire la concernant 
    async def prix(self,ctx, arg):
        planete = ["Terre","Lune","Mars","Venus","Mercure","Jupiter","Saturne","Neptune","Uranus","Pluton","Autre"]
        embedPrincipal = discord.Embed(color=0x00ff00)
        embedPrincipal.set_thumbnail(url="https://www.crushpixel.com/big-static14/preview4/planet-space-with-stars-shiny-1674010.jpg")

        arg = formatNomPlanete(arg)
    
        assert arg in planete, await ctx.send(embed = discord.Embed(title = "Veuiller verifier l'orthogrape du nom de votre planete"))  # verif que la planete existe

        await ctx.send(embed=getEmbed(embedPrincipal,arg))

    @discord.slash_command(
        name="satellites",
        description="Liste des satellites de la planete choisis et de leur prix",
    ) # Fonction permettant de renvoyer toutes les lunes d'une planete 
    async def satellite(self,ctx, arg):
        planete = ["Terre","Lune","Mars","Venus","Mercure","Jupiter","Saturne","Neptune","Uranus","Pluton","Autre"]
        nomPlaneteSatellite = ["Mars","Jupiter","Saturne","Neptune","Uranus"]
        embeded = discord.Embed(color=0x00ff00)
        embeded.set_thumbnail(url="https://www.crushpixel.com/big-static14/preview4/planet-space-with-stars-shiny-1674010.jpg")

        arg = formatNomPlanete(arg)
        assert arg in planete, await ctx.send(embed = discord.Embed(title = "Veuiller verifier l'orthogrape du nom de votre planete !")) # verif que la planete existe
        assert arg in nomPlaneteSatellite, await ctx.send(embed = discord.Embed(title = "Il n'y a pas de satellite pour cette Planete !")) # verif que la planete as un satellite
    
        cur = GetPrixSatellite(arg)
    
        embeded.title="Satellites de __{}__".format(arg)
    
        for row in cur:
       
            embeded.add_field(name="{}".format(row[0]), value="{}".format(convert(row[1])), inline=False)

        await ctx.send(embed = embeded)


def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(CogMission(bot))
