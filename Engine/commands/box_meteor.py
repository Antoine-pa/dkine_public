from time import time
from random import randint
from asyncio import sleep

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


class CogBoxMeteor(commands.Cog, functions.Func):
	def __init__(self, client):
		self.client = client
		functions.Func.__init__(self, client)

	@commands.command()
	async def box(self, ctx):
		try:
			timestamp = int(time()) #récupératon de timestamp
			randomtime = randint(600, 1200) #random time de la prochaine box
			user_id = ctx.author.id #récupération de l'id du joueur
			box = self.select_db(table = "`t-d-convois`", fields = "`c-convois`")
			msg_box = {
				"fr_box" : "GG a toi!!!\nTu viens de récupérer la box dans laquelle tu viens de gagner :",
				"en_box" : "[en message]",
				"it_box" : "[it message]",
				"fr_no_box" : "Nous ne savons pas encore quand arrive la box.\nNous le saurons 3min avant son arrivé. Redemandez tout à l'heure!",
				"en_no_box" : "[en message]",
				"it_no_box" : "[it message]"
				}          
			result = await self.verif(ctx = ctx, UserId = user_id)
			
			if result == False:
				return
			else:
				lang = result
				
			if box == []:
				self.insert_db(table = "`t-d-convois`", fields = "`c-convois`", values = f"{timestamp + randomtime}")
				#logs:
				await self.Logs(channel = 749958210131329044, embed_msg = f"box récupéré par **{ctx.author}** depuis le serveur **{ctx.guild}**\n[permier enregistrement]", footer_msg = f"user id : {ctx.author.id},\nserver id : {ctx.guild.id}")
				#message:
				await self.Embed(ctx = ctx, msg = msg_box.get(f"{lang}_box"), color = rouge)
				
			else:
				box = box[0][0]
				
				if timestamp > box: #vérification qu'on peut récupérer la box
					self.update_db(table = "`t-d-convois`", data = f"`c-convois` = {timestamp + randomtime}")
					#logs:
					diftimstampbox = timestamp - box #récupération du temps avant la récupération de la box par celui qui l'a eu
					await self.Logs(channel = 749958210131329044, embed_msg = f"box récupéré par **{ctx.author}** depuis le serveur **{ctx.guild}**, avec un temps de {diftimstampbox}s apres la fin de l'encienne box.", footer_msg = f"user id : {ctx.author.id},\nserver id : {ctx.guild.id}")
					#message:
					await self.Embed(ctx = ctx, msg = msg_box.get(f"{lang}_box"), color = rouge)
					
				else:
					if box - 180 > timestamp: #vérification qu'on peut voir le temps restant avant la box. si non:
						await self.Embed(ctx = ctx, msg = msg_box.get(f"{lang}_no_box"), color = rouge)
						
					else: #si oui:
						seconds = box - timestamp
						minutes = seconds // 60
						seconds %= 60
						
						msg_box_time = {
							"fr_time_box" : f"D'apres nos informations, la box arrivera dans {seconds}:{minutes}.",
							"en_time_box" : "[en message]",
							"it_time_box" : "[it message]"
							}
						await self.Embed(ctx = ctx, msg = msg_box_time.get(f"{lang}_time_box"), color = rouge)                        
		except MC.Error as err:
			print(err)
			
	@commands.command()
	async def meteor(self, ctx):
		try:
			user_id = ctx.author.id
			result = await self.verif(ctx = ctx, UserId = user_id)
			if result == False:
				return
			else:
				lang = result
			timestamp = int(time()) #récupératon de timestamp
			informations = self.select_db(table = "`t-d-meteor`", fields = "*")

			if informations == []:
				timestamp = int(time())
				tdp = timestamp + randint(5, 10) #timestamp debut pluie
				tfp = tdp + randint(20, 40) #timestamp fin pluie
				tdm = tdp + randint(1, 5) #timestamp debut meteor
				tfm = tdm + randint(5, 10)
				if tdp < tdm < tfm < tfp:
					self.insert_db(table = "`t-d-meteor`", fields = "`m-meteorshower-start`, `m-meteorshower-end`, `m-arrive-meteor`, `m-leave-meteor`", values = f"{tdp}, {tfp}, {tdm}, {tfm}")
			else:
				tdp, tfp, tdm, tfm = informations[0][0], informations[0][1], informations[0][2], informations[0][3]

			if tdp <= timestamp < tfp: #si il y a une pluie
				await ctx.channel.send("il y a une pluie")
				if tdm <= timestamp < tfm: #si il y a une météorite
					await ctx.channel.send("il y a un météor")
					tdm = timestamp + randint(5, 7)
					tfm = tdm + randint(5, 7)
					self.update_db(table = "`t-d-meteor`", data = f"`m-arrive-meteor` = {tdm}, `m-leave-meteor` = {tfm}")

				else: #si il n'y a pas de météorite
					await ctx.channel.send("pas encore de météor")


			else: #si il n'y a pas de pluie
				await ctx.channel.send("pas de pluie")
		except MC.Error as err:
			print(err)
			
def setup(client):
	client.add_cog(CogBoxMeteor(client))
