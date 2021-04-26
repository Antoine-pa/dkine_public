from time import time
from random import randint

import discord
from discord.ext import commands
import mysql.connector as MC

#pylint: disable=import-error
import sys
sys.path.append("../..")
import Engine.utility.functions as functions

bleu = 0x00FFFF #moderation part

class CogOnReady(commands.Cog, functions.Func):
	def __init__(self, client):
		self.client = client
		functions.Func.__init__(self, client)
		
	@commands.Cog.listener() #launch event
	async def on_ready(self):
		try:
			await self.Logs(channel = 747073930547691551, embed_msg = "`bot on`")
			
			t_d_meteor = self.select_db(table = "`t-d-meteor`", fields = "`m-meteorshower-start`, `m-meteorshower-end`, `m-arrive-meteor`, `m-leave-meteor`")
			if t_d_meteor == []: #si rien n'est save
				timestamp = int(time())
				tdp = timestamp + randint(5, 10) #timestamp debut pluie
				tfp = tdp + randint(20, 40) #timestamp fin pluie
				tdm = tdp + randint(1, 5) #timestamp debut meteor
				tfm = tdm + randint(5, 10)
				if tdp < tdm < tfm < tfp:
					self.insert_db(table = "`t-d-meteor`", fields = "`m-meteorshower-start`, `m-meteorshower-end`, `m-arrive-meteor`, `m-leave-meteor`", values = f"{tdp}, {tfp}, {tdm}, {tfm}")

			nb_serveur = self.select_db(table = "`t-d-serv`", fields = "`s-server-id`")
			nb_players = self.select_db(table = "`t-d-users`", fields = "`user-id`")
			presence = f"{len(self.client.guilds)} servers, {len(nb_players)} players"
			await self.client.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = presence))


			try:
				for guild in self.client.guilds:
					if (guild.id,) not in nb_serveur:
						self.insert_db(table = "`t-d-serv`", fields = "`s-server-id`", values = f"{guild.id}")
			except IndexError:
				for guild in self.client.guilds:
					self.insert_db(table = "`t-d-serv`", fields = "`s-server-id`", values = f"{guild.id}")
			print("start")
		except MC.Error as err:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
			print(err)
def setup(client):
	client.add_cog(CogOnReady(client))