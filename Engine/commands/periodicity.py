import discord
from discord.ext import commands
import mysql.connector as MC
import time
import random

#pylint: disable=import-error
import sys
sys.path.append("../..")
import Engine.utility.functions as functions

rouge = 0xCC0000 #game part
bleu = 0x00FFFF #partie modération
account = True

class CogPeriodicity(commands.Cog, functions.Func):
	def __init__(self, client):
		self.client = client
		functions.Func.__init__(self, client)      
		
	@commands.command()
	async def weekly(self, ctx):
		try:
			user_id = ctx.author.id
			timestamp = int(time.time())
			weekly = self.select_db(table = "`t-d-timestamp`", fields = "`t-weekly`", condition = f"`t-user-id` = {user_id}")
			msg_weekly = {
				"fr_weekly" : "Vous venez de récupérer votre weekly. Vous gagnez :",
				"en_weekly" : "[en message]",
				"it_weekly" : "[it message]"
				}
			lang = ""
			
			result = await self.verif(ctx = ctx, UserId = user_id)
			if result == False:
				return
			else:
				lang = result
			if weekly[0][0] == 0 or weekly[0][0] < timestamp:
				timestamp += 604800
				self.update_db(table = "`t-d-timestamp`", data = f"`t-weekly` = {timestamp}", condition = f"`t-user-id` = {user_id}")
				await self.Embed(ctx = ctx, msg = msg_weekly[f"{lang}_weekly"], color = rouge)
				
				#logs:
				logs_msg = {
					"msg_log" : f"weekly récupéré par **{ctx.author}** depuis le serveur **{ctx.guild}**",
					"msg_footer" : f"user id : {ctx.author.id},\nserver id : {ctx.guild.id}"
					}
				await self.Logs(channel = 736623245037535252, embed_msg = logs_msg.get("msg_log"), footer_msg = logs_msg.get("msg_footer"))
			else:
				seconds = weekly[0][0] - int(time.time())
				minutes = seconds // 60
				seconds %= 60
				hours = minutes // 60
				minutes %= 60
				days = hours // 24
				hours %= 24
				msg_weekly_error = {
					"fr_weekly_error" : f"Tu ne peux récupérer ton weekly que dans {days} jours, {hours} heures, {minutes} minutes et {seconds} secondes.",
					"en_weekly_error" : "[en message]",
					"it_weekly_error" : "[it message]"
					 }
				await self.Embed(ctx = ctx, msg = msg_weekly_error.get(f"{lang}_weekly_error"), color = rouge)
		except MC.Error as err:
			print(err)
	@commands.command()
	async def daily(self, ctx):
		try:
			user_id = ctx.author.id
			timestamp = int(time.time())
			daily = self.select_db(table = "`t-d-timestamp`", fields = "`t-daily`", condition = f"`t-user-id` = {user_id}")
			msg_daily = {
				"fr_daily" : "Vous venez de récupérer votre daily. Vous gagnez :",
				"en_daily" : "[en message]",
				"it_daily" : "[it message]"
				}
			result = await self.verif(ctx = ctx, UserId = user_id)
			if result == False:
				return
			else:
				lang = result
			if daily[0][0] == 0 or daily[0][0] < timestamp:
				timestamp += 86400
				self.update_db(table = "`t-d-timestamp`", data = f"`t-daily` = {timestamp}", condition = f"`t-user-id` = {user_id}")
				await self.Embed(ctx = ctx, msg = msg_daily.get(f"{lang}_daily"), color = rouge)
				#logs:
				logs_msg = {
					"msg_log" : f"daily récupéré par **{ctx.author}** depuis le serveur **{ctx.guild}**",
					"msg_footer" : f"user id : {ctx.author.id},\nserver id : {ctx.guild.id}"
					}
				await self.Logs(channel = 736623187764314302, embed_msg = logs_msg.get("msg_log"), footer_msg = logs_msg.get("msg_footer"))
			else:
				seconds = daily[0][0] - int(time.time())
				minutes = seconds // 60
				seconds %= 60
				hours = minutes // 60
				minutes %= 60
				#"-------------------"
				msg_daily_error = {
					"fr_daily_error" : f"Tu ne peux récupérer ton daily que dans {hours} heures, {minutes} minutes et {seconds} secondes.",
					"en_daily_error" : "[en message]",
					"it_daily_error" : "[it message]"
					}
				await self.Embed(ctx = ctx, msg = msg_daily_error.get(f"{lang}_daily_error"), color = rouge)
		except MC.Error as err:
			print(err)
			
	@commands.command()
	async def tax(self, ctx):
		try:
			user_id = ctx.author.id
			timestamp = int(time.time())
			randomtime = random.randint(1800, 7200)
			tax = self.select_db(table = "`t-d-timestamp`", fields = "`t-tax`", condition = f"`t-user-id` = {user_id}")
			msg_tax = {
				"fr_tax" : "Vous venez de récupérer votre tax. Vous gagnez :",
				"en_tax" : "[en message]",
				"it_tax" : "[it message]"
				}
			lang = ""
			result = await self.verif(ctx = ctx, UserId = user_id)
			if result == False:
				return
			else:
				lang = result
			if tax[0][0] == 0 or tax[0][0] < timestamp:
				timestamp += randomtime
				self.update_db(table = "`t-d-timestamp`", data = f"`t-tax` = {timestamp}", condition = f"`t-user-id` = {user_id}")
				await self.Embed(ctx = ctx, msg = msg_tax.get(f"{lang}_tax"), color = rouge)
				#logs:
				logs_msg = {
					"msg_log" : f"Tax récupéré par **{ctx.author}** depuis le serveur **{ctx.guild}**",
					"msg_footer" : f"user id : {ctx.author.id},\nserver id : {ctx.guild.id}"
					}
				await self.Logs(channel = 736623131854372958, embed_msg = logs_msg.get("msg_log"), footer_msg = logs_msg.get("msg_footer"))
			else:
				seconds = tax[0][0] - int(time.time())
				minutes = seconds // 60
				seconds %= 60
				hours = minutes // 60
				minutes %= 60
				#"-------------------"
				msg_tax_error = {
					"fr_tax_error" : f"Tu ne peux récupérer tes taxes que dans {hours} heures, {minutes} minutes et {seconds} secondes.",
					"en_tax_error" : "[en message]",
					"it_tax_error" : "[it message]"
					}
				await self.Embed(ctx = ctx, msg = msg_tax_error.get(f"{lang}_tax_error"), color = rouge)
		except MC.Error as err:
			print(err)

	@commands.command() #MissingRequiredArgument
	async def rep(self, ctx, user : discord.User):
		try:
			user_id = ctx.author.id
			timestamp = int(time.time())
			rep = self.select_db(table = "`t-d-timestamp`", fields = "`t-rep`", condition = f"`t-user-id` = {user_id}")[0][0]
			rep_user = self.select_db(table = "`t-d-profile`", fields = "`p-rep`", condition = f"`p-id` = {user.id}")[0][0]
			msg_rep = {
				"fr_rep" : "[fr message]",
				"en_rep" : "[en message]",
				"it_rep" : "[it message]",

				"fr_recipient_err" : "",
				"en_recipient_err" : "",
				"it_recipient_err" : ""
				}
			result = await self.verif(ctx = ctx, UserId = user_id)
			if result == False:
				return
			else:
				lang = result
			result = await self.verif_recipient(ctx = ctx, UserId = user.id)
			if result == False:
				return
			if ctx.author.id != user.id: #si il s'auto envoit pas un rep
				if rep == 0 or rep < timestamp: #si il peut envoyer son rep
					timestamp += 86400
					self.update_db(table = "`t-d-timestamp`", data = f"`t-rep` = {timestamp}", condition = f"`t-user-id` = {user_id}")
					self.update_db(table = "`t-d-profile`", data = f"`p-rep` = {rep_user + 1}", condition = f"`p-id` = {user.id}")
					await self.Embed(ctx = ctx, msg = msg_rep.get(f"{lang}_rep"), color = rouge)
					#logs:
					logs_msg = {
						"msg_log" : f"rep envoyé par **{ctx.author}** depuis le serveur **{ctx.guild}** à **{user.name}**",
						"msg_footer" : f"user id : {ctx.author.id} ==> {user.id},\nserver id : {ctx.guild.id}"
						}
					await self.Logs(channel = 754753245125148673, embed_msg = logs_msg.get("msg_log"), footer_msg = logs_msg.get("msg_footer"))

				else:
					seconds = rep - int(time.time())
					minutes = seconds // 60
					seconds %= 60
					hours = minutes // 60
					minutes %= 60
					msg_rep_error = {
						"fr_rep_error" : f"Tu ne peux renvoyer ton point de réputation que dans {hours} heures, {minutes} minutes et {seconds} secondes.",
						"en_rep_error" : "[en message]",
						"it_rep_error" : "[it message]"
						}
					await self.Embed(ctx = ctx, msg = msg_rep_error.get(f"{lang}_rep_error"), color = rouge)
		except MC.Error as err:
			print(err)
			
def setup(client):
	client.add_cog(CogPeriodicity(client))
