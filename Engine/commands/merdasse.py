import discord
from discord.ext import commands, tasks
import mysql.connector as MC
import asyncio

#pylint: disable=import-error
import sys
sys.path.append("../..")
import Engine.utility.functions as functions


rouge = 0xCC0000 #partie jeu
bleu = 0x00FFFF #partie modération


class CogMerdasse(commands.Cog, functions.Func):
	def __init__(self, client):
		self.client = client
		functions.Func.__init__(self, client)
		

	@commands.command() #ping command
	async def ping(self, ctx):
		msg = {"ping" : f"Pong! {self.pong}\n{round(self.client.latency * 1000)} ms"}
		await ctx.channel.send(msg.get("ping"))
		
	@commands.command()
	async def report(self, ctx, *msg_report):
		msgs_report = {
			"fr" : f"Tout contenu inaproprié sera punis d'un ban game.\nValidation : {self.yes}\nAnnulation : {self.no}",
			"en" : f"",
			"it" : f""
			}
		user_id = ctx.author.id
		lang = ""
		result = await self.verif(ctx = ctx, UserId = user_id)
		if result == False:
			return
		else:
			lang = result
		message = await self.Embed(ctx = ctx, msg = msgs_report.get(lang), color = rouge, ret = True)
		await message.add_reaction(self.yes)
		await message.add_reaction(self.no)
		def checkEmoji(reaction, user):
			return ctx.message.author == user and message.id == reaction.message.id and (str(reaction.emoji) == self.yes or str(reaction.emoji) == self.no)
		try:
			reaction, user = await self.client.wait_for("reaction_add", timeout = 10, check = checkEmoji)
			if reaction.emoji == self.yes:
				await self.Logs(channel = 749720903054524486, embed_msg = " ".join(msg_report), footer_msg = f"user : {ctx.author} ({ctx.author.id})\nguild : {ctx.guild} ({ctx.guild.id})")
				await self.Embed(ctx = ctx, msg = "Repport de beug validé.", color = rouge)
			else:
				await self.Embed(ctx = ctx, msg = "Vous avez annulé votre repport de beug.", color = rouge)
		except:
			pass

	@commands.command() #invitation command
	async def invite(self, ctx):
		user_id = ctx.author.id
		msg_invit = { #dico messages
			"fr_serv_dkine" : "Viens rejoindre le serveur officiel de DkineBot! Ce sera avec plaisir que nous t'accueillerons.", "fr_serv_dkine_lien" : "https://discord.gg/xJcVnPq",
			"fr_inv_dkine" : "Lien pour inviter DkineBot sur un de tes serveurs:", "fr_inv_dkine_lien" : "https://discord.com/api/oauth2/authorize?client_id=729051372628213850&permissions=8&scope=bot",
			"fr_serv_strike" : "Voici un lien vers notre partenaire StrikeBot. Cet un jeu du même type que Dkine alors rejoins vite!", "fr_serv_strike_lien" : "[lien]",
			"fr_inv_strike" : "Lien pour inviter StrikeBot sur un de tes serveurs: ", "fr_inv_strike_lien" : "[lien]",

			"en_serv_dkine" : "[en message]", "en_serv_dkine_lien" : "https://discord.gg/xJcVnPq",
			"en_inv_dkine" : "[en message]", "en_inv_dkine_lien" : "https://discord.com/api/oauth2/authorize?client_id=729051372628213850&permissions=8&scope=bot",
			"en_serv_strike" : "[en message]", "en_serv_strike_lien" : "[lien]",
			"en_inv_strike" : "[en message]", "en_inv_strike_lien" : "[lien]",

			"it_serv_dkine" : "[it message]", "it_serv_dkine_lien" : "https://discord.gg/xJcVnPq",
			"it_inv_dkine" : "[it message]", "it_inv_dkine_lien" : "https://discord.com/api/oauth2/authorize?client_id=729051372628213850&permissions=8&scope=bot",
			"it_serv_strike" : "[it message]", "it_serv_strike_lien" : "[lien]",
			"it_inv_strike" : "[it message]", "it_inv_strike_lien" : "[lien]",
			}
		lang = ""      
		result = await self.verif(ctx = ctx, UserId = user_id)
		if result == False:
			return
		else:
			lang = result
		embed = discord.Embed(color = rouge)
		embed.add_field(name = msg_invit.get(f"{lang}_serv_dkine"), value = msg_invit.get(f"{lang}_serv_dkine_lien"), inline = False)
		embed.add_field(name = msg_invit.get(f"{lang}_inv_dkine"), value = msg_invit.get(f"{lang}_inv_dkine_lien"), inline = False)
		embed.add_field(name = msg_invit.get(f"{lang}_serv_strike"), value = msg_invit.get(f"{lang}_serv_strike_lien"), inline = False)
		embed.add_field(name = msg_invit.get(f"{lang}_inv_strike"), value = msg_invit.get(f"{lang}_inv_strike_lien"), inline = False)
		await ctx.channel.send(embed = embed)
		
	@commands.command() #laguage command
	async def lang(self, ctx, language):
		try:
			user_id = ctx.author.id
			msg_change_lang = { #dico messages
				"fr_change_error" : "entre un argument valide [en, fr, it]",
				"en_change_error" : "[en message]",
				"it_change_error" : "[en message]"
				}
			lang = ""
			result = await self.verif(ctx = ctx, UserId = user_id)
			if result == False:
				return
			else:
				lang = result

			if language in ("en", "it", "fr"):
				self.update_db(table = "`t-d-users`", data = f'`user-lang` = "{language}"', condition = f"`user-id` = {user_id}")
				embed = discord.Embed(description = f"langue : {language}", color = rouge)
				await ctx.channel.send(embed = embed)
			else:
				embed = discord.Embed(description = msg_change_lang.get(f"{lang}_change_error"), color = rouge) #bad argument
				await ctx.channel.send(embed = embed)
		except MC.Error as err:
			print(err)
			
	@commands.command()
	async def cost(self, ctx, object, number : int, lvl = None):
		if lvl is None:
			lvl = self.select_db(table = "`t-d-profile`", fields = "*", condition = f"`p-id` = {ctx.author.id}")[0][self.dico_index_db_profile["lvl"]]
		else:
			lvl = int(lvl)
		dico = self._cost(object = object, number = number, lvl_player = lvl)
		msg = ""
		for value in dico.items():
			msg += f"\n{value[0]} : {value[1]}"
		await ctx.send(msg)
		
def setup(client):
	client.add_cog(CogMerdasse(client))
