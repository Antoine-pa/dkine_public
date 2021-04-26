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

class CogTrade(commands.Cog, functions.Func):
	def __init__(self, client):
		self.client = client
		functions.Func.__init__(self, client)

	@commands.command()
	async def give(self, ctx, ress, numb, user : discord.User):
		try:
			user_id = ctx.author.id
			result = await self.verif(ctx = ctx, UserId = user_id)
			if result == False:
				return
			else:
				lang = result
			result = await self.verif_recipient(ctx = ctx, UserId = user.id)
			if result == False:
				return
				
			"""
			result = self.what_ress(ctx, ress)
			if result == False:
				return
			else:
				ress = result
			result = self.number(ctx, numb)
			if result == False:
				return
			else:
				numb = result #numb est de typer integer
			"""
			numb = int(numb)
			ress_output_sender = self.select_db(table = "`t-d-profile`", fields = f"`p-{ress}`", condition = f"`p-id` = {user_id}")[0][0]

			if numb > ress_output_sender:
				await ctx.send("tu n'as pas assez de ressource")
				return

			ress_input_sender = ress_output_sender - numb
			self.update_db(table = "`t-d-profile`", data = f'`p-{ress}` = {ress_input_sender}', condition = f'`p-id` = {user_id}')
			ress_output_recipient = self.select_db(table = "`t-d-profile`", fields = f"`p-{ress}`", condition = f"`p-id` = {user.id}")[0][0]
			ress_input_recipient = ress_output_recipient + numb
			self.update_db(table = "`t-d-profile`", data = f'`p-{ress}` = {ress_input_recipient}', condition = f'`p-id` = {user.id}')

			await self.Embed(ctx = ctx, msg = f"Vous venez d'envoyer {numb} {ress} a {user}", color = rouge)
			
		except MC.Error as err:
			print(err)

def setup(client):
	client.add_cog(CogTrade(client))