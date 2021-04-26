import discord
from discord.ext import commands
import mysql.connector as MC

#pylint: disable=import-error
import sys
sys.path.append("../..")
import Engine.utility.functions as functions

class CogRecrute(commands.Cog, functions.Func):
	def __init__(self, client):
		functions.Func.__init__(self, client)
		self.client = client

	@commands.command()
	async def train(self, ctx, unite, number):

		def checkEmoji(reaction, user):
			return ctx.message.author == user and message.id == reaction.message.id and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌")

		user_id = ctx.author.id
		result = await self.verif(ctx = ctx, UserId = user_id)
		if result == False:
			return
		else:
			lang = result

		if not number.isdigit():
			#send msg erreur, invalide syntaxe
			return
		if unite not in ("soldat", "soldats", "archer", "archers", "mage", "mages"):
			#msg erreur syntaxe
			return
		if unite in ("soldats", "archers", "mages"):
			unite = unite[:-1]
		number = int(number)

		table_user = self.select_db(table = "`t-d-profile`", fields = "*", condition = f"`p-id` = {ctx.author.id}") #les autres ressources

		cout = None
		#if assez de ressources:
		message = await ctx.send(f"confirmes tu la formation de {number} {unite} pour un coût de {cout}?")
		await message.add_reaction("✅")
		await message.add_reaction("❌")
		try:
			reaction, _  = await self.client.wait_for("reaction_add", timeout = 20, check = checkEmoji)
		except:
			await ctx.send("tu n'as pas validé ta formation avec la réaction ✅")
		if reaction.emoji == "✅":
			await ctx.send("la formation a été lancée")
		else:
			await ctx.send("vous avez annulé la formation")
		#update ressources db + timestamp formation
		
	@commands.command()
	async def make(self, ctx, engine, number):

		def checkEmoji(reaction, user):
			return ctx.message.author == user and message.id == reaction.message.id and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌")
		
		user_id = ctx.author.id
		result = await self.verif(ctx = ctx, UserId = user_id)
		if result == False:
			return
		else:
			lang = result

		if not number.isdigit():
			await ctx.send("Syntaxe invalide")
			return
		if engine not in ("machine", "machines"):
			await ctx.send("L'engin que tu veux construire n'existe pas")
			return
		if engine in ("machines"):
			engine = engine[:-1]
		number = int(number)

		table_user = self.select_db(table = "`t-d-profile`", fields = "*", condition = f"`p-id` = {ctx.author.id}") #les autres ressources

		cout = None
		#if assez de ressources:
		message = await ctx.send(f"confirmes tu la fabrication de {number} {engine} pour un coût de {cout}?")
		await message.add_reaction("✅")
		await message.add_reaction("❌")
		try:
			reaction, _  = await self.client.wait_for("reaction_add", timeout = 20, check = checkEmoji)
		except:
			await ctx.send("tu n'as pas validé ta fabrication avec la réaction ✅")
		if reaction.emoji == "✅":
			await ctx.send("la production a été lancée")
		else:
			await ctx.send("vous avez annulé la fabrication")
		#update ressources db + timestamp formation

def setup(client):
	client.add_cog(CogRecrute(client))