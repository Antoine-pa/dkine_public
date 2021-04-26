import random

import discord
from discord.ext import commands
import mysql.connector as MC 

#pylint: disable=import-error
import sys
sys.path.append("../..")
import Engine.utility.functions as functions

rouge = 0xCC0000 #game part
vert = 0x00CC00 #confirmation part
bleu = 0x00FFFF #moderation part
alias_profile = ["p", "P", "PROFILE", "pr"]

class CogProfile(commands.Cog, functions.Func):
	def __init__(self, client):
		self.client = client
		functions.Func.__init__(self, client)
		
	@commands.command(aliases = alias_profile)
	async def profile(self, ctx): #profile opening command
		max_humeur = 80
		user_id = ctx.author.id
		result = await self.verif(ctx = ctx, UserId = user_id)
		if result == False:
			return
		else:
			lang = result
		data_p = self.select_db(table = "`t-d-profile`", fields = "*", condition = f"`p-id` = {user_id}")[0]
		msg_p = { #dico messages
			"fr-lvl" : f"PROFIL DE {ctx.author.name}", "fr-lvl-affi" : f"> niveau {data_p[self.dico_index_db_profile['lvl']]}\n>   | xp : {data_p[self.dico_index_db_profile['xp']]}/???",
			"fr-nat" : "\nNATION:", "fr-nat-affi" : f"> 👭 | population : {data_p[self.dico_index_db_profile['population']]}\n> ♋ | humeur : {data_p[self.dico_index_db_profile['mood']]}/{max_humeur}",
			"fr-min" : "\nMINÉRAUX:", "fr-min-affi" : f"> 💰 | or : {data_p[self.dico_index_db_profile['gold']]}\n> 🔩 | fer : {data_p[self.dico_index_db_profile['iron']]}\n> ⚙ | charbon : {data_p[self.dico_index_db_profile['coal']]}\n> 🧱 | pierre : {data_p[self.dico_index_db_profile['stone']]}\n> ☄ | météorites : {data_p[self.dico_index_db_profile['meteor']]}\n> 🏵️ | runes : {data_p[self.dico_index_db_profile['rune']]}",
			"fr-ress" : "\nRESSOURCES:", "fr-ress-affi" : f"> 🌲 | bois : {data_p[self.dico_index_db_profile['wood']]}\n> 🟫 | cuir : {data_p[self.dico_index_db_profile['leather']]}\n> 🍗 | nourriture : {data_p[self.dico_index_db_profile['food']]}",
			"fr-mili" : "\nMILITAIRE:", "fr-mili-affi" : f"> 🗡 | soldats : {data_p[self.dico_index_db_profile['soldat']]}\n> 🏹 | archers : {data_p[self.dico_index_db_profile['archer']]}\n> 🏹 | machines : {data_p[self.dico_index_db_profile['machine']]}\n> 🧙 | mage : {data_p[self.dico_index_db_profile['mage']]}\n> ⛵ | bateaux : {data_p[self.dico_index_db_profile['boat']]}\n> ⚡ | énergie : {data_p[self.dico_index_db_profile['energy']]}",
			"fr-bat" : "\nBÂTIMENTS:", "fr-bat-affi" : f"> ⛏ | mine : {data_p[self.dico_index_db_profile['mine']]}\n> 🌾 | nombre de ferme : {data_p[self.dico_index_db_profile['town']]}\n> 🌾 | nombre de mine de lave : {data_p[self.dico_index_db_profile['lava-mine']]}\n> 🏭 | niveau d'atelier : {data_p[self.dico_index_db_profile['workshop']]}\n> 🏭 | niveau de la caserne : {data_p[self.dico_index_db_profile['caserne']]}",

			"en-lvl" : f"PROFILE OF {ctx.author.name}", "en-lvl-affi" : f"> {data_p[self.dico_index_db_profile['lvl']]}",
			"en-nat" : "[en title]", "en-nat-affi" : "[en message]",
			"en-min" : "[en title]", "en-min-affi" : "[en message]",
			"en-ress" : "[en title]", "en-ress-affi" : "[en message]",
			"en-mili" : "[en title]", "en-mili-affi" : "[en message]",
			"en-bat" : "[en title]", "en-bat-affi" : "[en message]",

			"it-lvl" : f" {ctx.author.name}", "it-lvl-affi" : f"> niveau {data_p[self.dico_index_db_profile['lvl']]}",
			"it-nat" : "[it title]", "it-nat-affi" : "[it message]",
			"it-min" : "[it title]", "it-min-affi" : "[it message]",
			"it-ress" : "[it title]", "it-ress-affi" : "[it message]",
			"it-mili" : "[it title]", "it-mili-affi" : "[it message]",
			"it-bat" : "[it title]", "it-bat-affi" : "[it message]"
			}
		embed = discord.Embed(color = rouge) #embed 
		embed.add_field(name = msg_p[f"{lang}-lvl"], value = msg_p[f"{lang}-lvl-affi"], inline = True)
		embed.add_field(name = msg_p[f"{lang}-nat"], value = msg_p[f"{lang}-nat-affi"], inline = True)
		embed.add_field(name = msg_p[f"{lang}-min"], value = msg_p[f"{lang}-min-affi"], inline = True)
		embed.add_field(name = msg_p[f"{lang}-ress"], value = msg_p[f"{lang}-ress-affi"], inline = True)
		embed.add_field(name = msg_p[f"{lang}-mili"], value = msg_p[f"{lang}-mili-affi"], inline = True)
		embed.add_field(name = msg_p[f"{lang}-bat"], value = msg_p[f"{lang}-bat-affi"], inline = True)
		embed.set_footer(text = f"Resquested by {ctx.author.name}")
		await ctx.channel.send(embed = embed)
		
	@commands.command(aliases=["create", "st"]) #account creation command
	async def start(self, ctx):
		try:
			msg_new_compte = { #dico messages
				"start" : "**Nous sommes heureux de d'acueuillir comme nouveau joueurs!**\n[en message]\n[it message]\n\nNous espérons que je jeu vous plaira et vous ferra passer le temps. Toute les fonctionnalité de dkine sont détaillées grâce à la commande `!:help` ou `!:h`\n[en message]\n[it message].\n\nFais la commande `!:lang [en/fr/it]` pour définir une langue (la langue par défaut est l'anglais)\n[en message]\n[it message]",
				"fr-start-error" : "Tu possèdes déjà un compte.\nFais la commande `!:profile` pour l'afficher ou `!:help` si tu veux de l'aide",
				"en-start-error" : "[en message]",
				"it-start-error" : "[it message]"
				}
			user_id = ctx.author.id
			result = await self.verif_account(ctx = ctx, UserId = user_id, send_message = False)
			if not result:
				self.insert_db(table = "`t-d-users`", fields = "`user-id`, `user-date-creation`", values = f"{user_id}, NOW()") #setting up the users table info
				self.insert_db(table = "`t-d-profile`", fields = "`p-id`", values = f"{user_id}") #setting up profile table info
				self.insert_db(table = "`t-d-timestamp`", fields = "`t-user-id`", values = f"{user_id}") #setting up improvement table info, etc
				nb_players = self.select_db(table = "`t-d-users`", fields = "`user-id`")
				embed = discord.Embed(description = msg_new_compte.get("start"), color = rouge)
				await ctx.channel.send(embed = embed)
				await self.client.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = f"{len(self.client.guilds)} servers, {len(nb_players)} players")) #change in bot presence
			else:
				lang = result
				await self.Embed(ctx = ctx, msg = msg_new_compte.get(f"{lang}-start-error"), color = rouge)
		except MC.Error as err:
			print(err)
			
def setup(client):
	client.add_cog(CogProfile(client))
