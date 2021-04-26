import discord
from discord.ext import commands
import mysql.connector as MC

#pylint: disable=import-error
import sys
sys.path.append("../..")
import Engine.utility.functions as functions

bleu = 0x00FFFF
rouge = 0xCC0000
jaune = 0xFFB200

class CogHelp(commands.Cog, functions.Func):
	def __init__(self, client):
		functions.Func.__init__(self, client)
		self.client = client
		
	@commands.command()
	async def help(self, ctx, motif = "menu"):
		user_id = ctx.author.id
		msg_help = {
			"fr_menu" : "Bienvenue sur le menu d'aide.\n\nVoici les catégories de commande:\n\n> `!:help profile`\n> `!:help resources`",
			"fr_profile" : "Votre profile est votre inventaire de jeu (votre compte).\nVous pourrez ouvrir votre profile grâce à la commande `!:profile`. Vous verrez alors vos ressources aparaître.\n\nFais la commande `!:help resources` pour avoir plus d'information.",
			"fr_resources" : "Votre empire possède un grand nombre de ressource. Elles vous permetteront d'effectuer certaines action et c'est ce qu'on va voir si-dessous:\n\n\n>la population : c'est votre indicateur pour connaître votre population\n\n>l'humeur : c'est l'indicateur de joie de la population. Il est influencé par les taxes notament\n\n>les minéraux : vous pouvez récuperer des minéraux dans les mines. Ils vous servront notament pour la fabrication/amélioration.\n\n>les autres ressources : vous pourrez les avoir dans les fermes. ils vous servirioons notamment à nourrir votre population ou fabriquer des choses\n\n>la partie militaire : elle vous indiquera le nombre de troupe, votre puissance ou encore votre énergie pour les déplacement de troupe.\n\n>les bâtiments : c'est votre nombre de ferme, de mine et votre niveau d'atelier.",

			"en_menu" : "",
			"en_profile" : "",
			"en_resources" : "",

			"it_menu" : "",
			"it_profile" : "",
			"it_resources" : ""
			}
		lang = ""
		
		result = await self.verif(ctx = ctx, UserId = user_id)
		if result == False:
			return
		else:
			lang = result
			
		if motif == "menu":
			embed = discord.Embed(description = msg_help.get(f"{lang}_menu"), color = jaune)
			embed.set_footer(text = f"requested by {ctx.author.name}")
			await ctx.channel.send(embed = embed)
		if motif == "profile":
			embed = discord.Embed(description = msg_help.get(f"{lang}_profile"), color = jaune)
			embed.set_footer(text = f"requested by {ctx.author.name}")
			await ctx.channel.send(embed = embed)
		if motif == "resources":
			embed = discord.Embed(description = msg_help.get(f"{lang}_resources"), color = jaune)
			embed.set_footer(text = f"requested by {ctx.author.name}")
			await ctx.channel.send(embed = embed)
		if motif == "":
			pass
		
def setup(client):
	client.add_cog(CogHelp(client))
