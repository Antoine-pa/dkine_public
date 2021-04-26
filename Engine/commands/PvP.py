import time
import random

import discord
from discord.ext import commands, tasks
import mysql.connector as MC

#pylint: disable=import-error
import sys
sys.path.append("../..")
import Engine.utility.functions as functions
from Engine.utility.fight import Fight, Troop

dico_des_pv = 50 # à changer mais flemme

class CogPvP(commands.Cog, functions.Func):
	def __init__(self, client):
		self.client = client
		functions.Func.__init__(self, client)

	@commands.command()
	async def dep(self, ctx, zone = None, *, battaillon = None):

		def checkBattaillon(message):
			return message.author == ctx.message.author and ctx.channel == message.channel and (message.content.startswith("add") or message.content.startswith("del") or message.content.startswith("go") or message.content.startswith("stop"))

		def checkEmoji(reaction, user):
			return ctx.message.author == user and msg.id == reaction.message.id and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌" or str(reaction.emoji) == "↩️")

		def checkMsg(message):
			return message.author == ctx.message.author and ctx.channel == message.channel and message.content[0].upper() in ("A", "B", "C") and message.content[1:].isdigit()

		user_id = ctx.author.id
		result = await self.verif(ctx = ctx, UserId = user_id)
		if result == False:
			return
		else:
			lang = result

		msg_del = []
		data_p = self.select_db(table = "`t-d-profile`", fields = "*", condition = f"`p-id` = {user_id}")[0] #données du profile du joueur
		dico_value = {"soldat" : 0, "archer" : 0, "mage" : 0, "machine" : 0}

		if zone is None:
			msg = await ctx.send("sur quel zone voulez vous vous déployer:")
			msg_del.append(msg)
			while True:
				message = await self.client.wait_for("message", timeout = 120, check = checkMsg)
				message.content = message.content[0].upper() + message.content[1:]
				if message.content not in self.list_zone:
					await ctx.send("la zone resignée n'existe pas")
					continue
				zone = message.content
				data_m = self.select_db(table = "`t-d-maps`", fields = "*", condition = f"`m-map` = '{zone}'")[0]
				if data_m[self.dico_index_db_maps["user_id"]] != user_id:
					await ctx.send("la zone mentionnée ne vous appartient pas")
					continue
				break
		else:
			zone = zone[0].upper() + zone[1:]
			if zone not in self.list_zone:
				await ctx.send("la zone renseignée n'existe pas")
				return
			data_m = self.select_db(table = "`t-d-maps`", fields = "*", condition = f"`m-map` = '{zone}'")[0]
			if data_m[self.dico_index_db_maps["user_id"]] != user_id:
				await ctx.send("la zone mentionnée ne vous appartient pas")
				return



		if battaillon is not None:
			battaillon = battaillon.split(",")
			for value in battaillon:
				value = value.split()
				if len(value) != 2 or not value[1].isdigit() or value[0] not in ("soldat","soldats", "archer", "archers", "mage", "mages", "machine", "machines"):
					await ctx.send("syntaxe invalide dans le champs du battaillon")
					return
				if value[0] in ("soldats", "archers", "mages", "machines"):
					value[0] = value[0][:-1]
				if value[0] in dico_value: #si il y avait deja des troupes comme ca
					val = dico_value[value[0]] #on récup l'encienne valeur
					if val + int(value[1]) > data_p[self.dico_index_db_profile[value[0]]]:
						await ctx.send(f"tu n'as pas assez d'unité en réserve. Tu ne peux ajouter que {data_p[self.dico_index_db_profile[value[0]]] - val} {value[0]}{self.s((data_p[self.dico_index_db_profile[value[0]]] - val))}")
						return
					dico_value[value[0]] = val + int(value[1])
		else:
			_msg = await ctx.send("```Battaillon à déployer :```")
			msgg = [] #liste des troupes qu'il ajoute au combat
			

			for v in dico_value.items():
				msgg.append(f"{v[1]} {v[0]}{self.s(v[1])} : {v[1] * self.dico_puissances[v[0]]} de puissance")
			embed = discord.Embed(description = "\n".join(msgg), title = f"**--> {zone}**") # + "\n\ntotaux des puissances"
			await _msg.edit(embed = embed.set_footer(text = "-add [troupe] [nombre]\n-del [troupe] [nombre]\n-stop\n-go"))



			while True: #gestion du deploiement
				try:
					value = await self.client.wait_for("message", timeout = 120, check = checkBattaillon) #attente d'un add, del, go, stop
				except:
					await ctx.send("tu n'as pas validé ton deploiement avec le mot clé 'go'")
					for m in msg_del:
						await m.delete()
					msg_del = None
					return
				msg_del.append(value)



				if value.content.startswith("add"):
					value = value.content.split()[1:] #on récup,l'unité et le nombre
					if value[0] in ["soldat","soldats", "archer", "archers", "mage", "mages", "machine", "machines"] and value[1].isdigit(): #on vérif
						if value[0] in ["soldats", "archers", "mages", "machines"]: #on modif si nécessaire
							value[0] = value[0][:-1] #on modif si nécessaire
						if value[0] in dico_value: #si il y avait deja des troupes comme ca
							val = dico_value[value[0]] #on récup l'encienne valeur
							if val + int(value[1]) > data_p[self.dico_index_db_profile[value[0]]]:
								msg_del.append(await ctx.send(f"tu n'as pas assez d'unité en réserve. Tu ne peux ajouter que {data_p[self.dico_index_db_profile[value[0]]] - val} {value[0]}{self.s((data_p[self.dico_index_db_profile[value[0]]] - val))}"))
								continue
							dico_value[value[0]] = val + int(value[1]) #on add et on change

						msgg = []
						for v in dico_value.items():
							msgg.append(f"{v[1]} {v[0]}{self.s(v[1])} : {v[1] * self.dico_puissances[v[0]]} de puissance")
						embed = discord.Embed(description = "\n".join(msgg), title = f"**--> {zone}**") # + "\n\ntotaux des puissances"
						embed.set_footer(text = "-add [troupe] [nombre]\n-del [troupe] [nombre]\n-stop\n-go")
						await _msg.edit(embed = embed)
					else:
						msg_del.append(await ctx.send("Ajout incorect (mauvaise syntaxe)\nex : `add soldat 1`"))
						continue


				elif value.content.startswith("del"):
					value = value.content.split()[1:]
					if value[0] in ["soldat", "archer", "mage", "machine"] and value[1].isdigit():
						if value[0] in ["soldats", "archers", "mages", "machines"]:
							value[0] = value[0][:-1]
						if value[0] in dico_value:
							val = dico_value[value[0]]
							if val - int(value[1]) >= 0:
								dico_value[value[0]] = val - int(value[1])
							else:
								dico_value[value[0]] = 0
							msgg = []
							for v in dico_value.items():
								msgg.append(f"{v[1]} {v[0]}{self.s(v[1])} : {v[1] * self.dico_puissances[v[0]]} de puissance")
							embed = discord.Embed(description = "\n".join(msgg), title = f"**--> {zone}**") # + "\n\ntotaux des puissances"
							embed.set_footer(text = "-add [troupe] [nombre]\n-del [troupe] [nombre]\n-stop\n-go")
							await _msg.edit(embed = embed)
						else:
							msg_del.append(await ctx.send("Suppression impossible (vous n'avez pas déployé ce type d'unité)."))
							continue
					else:
						msg_del.append(await ctx.send("Supression incorect (mauvaise syntaxe)\nex : `del soldat 1`"))
						continue



				elif value.content == "go":
					msg = await ctx.send("Etes vous sûr d'envoyer vos troupes?")
					msg_del.append(msg)
					await msg.add_reaction("✅")
					await msg.add_reaction("❌")
					await msg.add_reaction("↩️")
					try:
						reaction, _  = await self.client.wait_for("reaction_add", timeout = 20, check = checkEmoji)
					except:
						await ctx.send("tu n'as pas validé ton déploiment avec la réaction ✅")
						return
					if reaction.emoji == "✅":
						await ctx.send("envoie des troupes et nettoyage du salon en cours...")
						for m in msg_del:
							await m.delete()
						break

					elif reaction.emoji == "↩️":
						msg_del.remove(msg)
						await msg.delete()
						continue
					else:
						await ctx.send("Vous avez anulez le deploiement.")
						for m in msg_del:
							await m.delete()
						msg_del = None
						return

				elif value.content == "stop": #on le supprime
					await ctx.send("Vous avez anulez le deploiement.")
					for m in msg_del:
						await m.delete()
					msg_del = None
					return
		await ctx.send(f"Vous avez envoyé vos troupes vers la zone {zone}.")

		req_profile = ""
		req_fields_moove = ""
		req_values_moove = ""
		for value in dico_value.items():
			req_profile += f"`p-{value[0]}` = {data_p[self.dico_index_db_profile[f'{value[0]}']] - value[1]}, "
			req_fields_moove += f"`{value[0]}`, "
			req_values_moove += f"{value[1]}, "

		req_profile = req_profile[:-2]
		req_fields_moove = req_fields_moove[:-2]
		req_values_moove = req_values_moove[:-2]

		#self.update_db(table = "`t-d-maps`", data = f'`m-soldat` = {data_m[self.dico_index_db_maps["soldat"]] + dico_value.get("soldat")}, `m-archer` = {data_m[self.dico_index_db_maps["archer"]] + dico_value.get("archer")}, `m-machine` = {data_m[self.dico_index_db_maps["machine"]] + dico_value.get("machine")}, `m-mage` = {data_m[self.dico_index_db_maps["mage"]] + dico_value.get("mage")}', condition = f'`m-map` = "{zone}"')
		self.update_db(table = "`t-d-profile`", data = req_profile, condition = f"`p-id` = {user_id}")
		self.insert_db(table = "`moove`", fields = f"`user-id`, `value`, `timestamp`, `channel`, `zone1`, `zone2`, {req_fields_moove}", values = f"{user_id}, 'dep', {round(time.time()) + self.dico_time['dep']}, {ctx.channel.id}, 'p', '{zone}', {req_values_moove}")

	@commands.command()
	async def rm(self, ctx, zone = None, *, battaillon = None):

		def checkBattaillon(message):
			return message.author == ctx.message.author and ctx.channel == message.channel and (message.content.startswith("add") or message.content.startswith("del") or message.content.startswith("go") or message.content.startswith("stop"))

		def checkEmoji(reaction, user):
			return ctx.message.author == user and msg.id == reaction.message.id and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌" or str(reaction.emoji) == "↩️")

		def checkMsg(message):
			return message.author == ctx.message.author and ctx.channel == message.channel and message.content[0].upper() in ("A", "B", "C") and message.content[1:].isdigit()

		user_id = ctx.author.id
		result = await self.verif(ctx = ctx, UserId = user_id)
		if result == False:
			return
		else:
			lang = result

		msg_del = []
		data_p = self.select_db(table = "`t-d-profile`", fields = "*", condition = f"`p-id` = {user_id}")[0] #données du profile du joueur
		dico_value = {"soldat" : 0, "archer" : 0, "mage" : 0, "machine" : 0}

		if zone is None:
			msg = await ctx.send("sur quel zone voulez vous vous récupérer des unités:")
			msg_del.append(msg)
			while True:
				message = await self.client.wait_for("message", timeout = 120, check = checkMsg)
				message.content = message.content[0].upper() + message.content[1:]
				if message.content not in self.list_zone:
					await ctx.send("la zone resignée n'existe pas")
					continue
				zone = message.content
				data_m = self.select_db(table = "`t-d-maps`", fields = "*", condition = f"`m-map` = '{zone}'")[0]
				if data_m[self.dico_index_db_maps["user_id"]] != user_id:
					await ctx.send("la zone mentionnée ne vous appartient pas")
					continue
				break
		else:
			zone = zone[0].upper() + zone[1:]
			if zone not in self.list_zone:
				await ctx.send("la zone renseignée n'existe pas")
				return
			data_m = self.select_db(table = "`t-d-maps`", fields = "*", condition = f"`m-map` = '{zone}'")[0]
			if data_m[self.dico_index_db_maps["user_id"]] != user_id:
				await ctx.send("la zone mentionnée ne vous appartient pas")
				return

		if battaillon is not None:
			battaillon = battaillon.split(",")
			for value in battaillon:
				value = value.split()
				
				if len(value) != 2 or not value[1].isdigit() or value[0] not in ("soldat","soldats", "archer", "archers", "mage", "mages", "machine", "machines"):
					await ctx.send("syntaxe invalide dans le champs du battaillon")
					return
				if value[0] in ("soldats", "archers", "mages", "machines"):
					value[0] = value[0][:-1]
				if value[0] in dico_value: #si il y avait deja des troupes comme ca
					val = dico_value[value[0]] #on récup l'encienne valeur
					if val + int(value[1]) > data_m[self.dico_index_db_maps[value[0]]]:
						await ctx.send(f"tu n'as pas assez d'unité en réserve. Tu ne peux ajouter que {data_m[self.dico_index_db_maps[value[0]]] - val} {value[0]}{self.s((data_m[self.dico_index_db_maps[value[0]]] - val))}")
						return
					dico_value[value[0]] = val + int(value[1])
		else:
			_msg = await ctx.send("```Battaillon à récupérer :```")
			msgg = [] #liste des troupes qu'il ajoute au combat
			

			for v in dico_value.items():
				msgg.append(f"{v[1]} {v[0]}{self.s(v[1])} : {v[1] * self.dico_puissances[v[0]]} de puissance")
			embed = discord.Embed(description = "\n".join(msgg), title = f"**{zone} -->**") # + "\n\ntotaux des puissances"
			await _msg.edit(embed = embed.set_footer(text = "-add [troupe] [nombre]\n-del [troupe] [nombre]\n-stop\n-go"))



			while True: #gestion du deploiement
				try:
					value = await self.client.wait_for("message", timeout = 120, check = checkBattaillon) #attente d'un add, del, go, stop
				except:
					await ctx.send("tu n'as pas validé ta récupération avec le mot clé 'go'")
					for m in msg_del:
						await m.delete()
					msg_del = None
					return
				msg_del.append(value)



				if value.content.startswith("add"):
					value = value.content.split()[1:] #on récup,l'unité et le nombre
					if value[0] in ["soldat","soldats", "archer", "archers", "mage", "mages", "machine", "machines"] and value[1].isdigit(): #on vérif
						if value[0] in ["soldats", "archers", "mages", "machines"]: #on modif si nécessaire
							value[0] = value[0][:-1] #on modif si nécessaire
						if value[0] in dico_value: #si il y avait deja des troupes comme ca
							val = dico_value[value[0]] #on récup l'encienne valeur
							if val + int(value[1]) > data_m[self.dico_index_db_maps[value[0]]]:
								msg_del.append(await ctx.send(f"tu ne peux pas récuperer des unitées qui n'existes pas. Tu ne peux reprendre que {data_m[self.dico_index_db_maps[value[0]]] - val} {value[0]}{self.s((data_m[self.dico_index_db_maps[value[0]]] - val))} unitées"))
								continue
							dico_value[value[0]] = val + int(value[1]) #on add et on change

						msgg = []
						for v in dico_value.items():
							msgg.append(f"{v[1]} {v[0]}{self.s(v[1])} : {v[1] * self.dico_puissances[v[0]]} de puissance")
						embed = discord.Embed(description = "\n".join(msgg), title = f"**{zone} -->**") # + "\n\ntotaux des puissances"
						embed.set_footer(text = "-add [troupe] [nombre]\n-del [troupe] [nombre]\n-stop\n-go")
						await _msg.edit(embed = embed)
					else:
						msg_del.append(await ctx.send("Récupération incorect (mauvaise syntaxe)\nex : `add soldat 1`"))
						continue



				elif value.content.startswith("del"):
					value = value.content.split()[1:]
					if value[0] in ["soldat", "archer", "mage", "machine"] and value[1].isdigit():
						if value[0] in ["soldats", "archers", "mages", "machines"]:
							value[0] = value[0][:-1]
						if value[0] in dico_value:
							val = dico_value[value[0]]
							if val - int(value[1]) >= 0:
								dico_value[value[0]] = val - int(value[1])
							else:
								dico_value[value[0]] = 0
							msgg = []
							for v in dico_value.items():
								msgg.append(f"{v[1]} {v[0]}{self.s(v[1])} : {v[1] * self.dico_puissances[v[0]]} de puissance")
							embed = discord.Embed(description = "\n".join(msgg), title = f"**{zone} -->**") # + "\n\ntotaux des puissances"
							embed.set_footer(text = "-add [troupe] [nombre]\n-del [troupe] [nombre]\n-stop\n-go")
							await _msg.edit(embed = embed)
						else:
							msg_del.append(await ctx.send("Suppression impossible (vous n'avez pas ce type d'unité)."))
							continue
					else:
						msg_del.append(await ctx.send("Supression incorect (mauvaise syntaxe)\nex : `del soldat 1`"))
						continue



				elif value.content == "go":
					msg = await ctx.send("Etes vous sûr de vouloir récupérer vos troupes?")
					msg_del.append(msg)
					await msg.add_reaction("✅")
					await msg.add_reaction("❌")
					await msg.add_reaction("↩️")
					try:
						reaction, _  = await self.client.wait_for("reaction_add", timeout = 20, check = checkEmoji)
					except:
						await ctx.send("tu n'as pas validé ton renvoie avec la réaction ✅")
						return
					if reaction.emoji == "✅":
						await ctx.send("Renvoie des troupes et nettoyage du salon en cours...")
						for m in msg_del:
							await m.delete()
						break

					elif reaction.emoji == "↩️":
						msg_del.remove(msg)
						await msg.delete()
						continue
					else:
						await ctx.send("Vous avez anulez le renvoie.")
						for m in msg_del:
							await m.delete()
						msg_del = None
						return

				elif value.content == "stop": #on le supprime
					await ctx.send("Vous avez anulez le renvoie.")
					for m in msg_del:
						await m.delete()
					msg_del = None
					return
		await ctx.send(f"Vous avez renvoyé vos troupes de la zone {zone} chez vous.")

		req_maps = ""
		req_fields_moove = ""
		req_values_moove = ""
		for value in dico_value.items():
			req_maps += f"`m-{value[0]}` = {data_m[self.dico_index_db_maps[f'{value[0]}']] - value[1]}, "
			req_fields_moove += f"`{value[0]}`, "
			req_values_moove += f"{value[1]}, "

		req_maps = req_maps[:-2]
		req_fields_moove = req_fields_moove[:-2]
		req_values_moove = req_values_moove[:-2]

		self.update_db(table = "`t-d-maps`", data = req_maps, condition = f'`m-map` = "{zone}"')
		self.insert_db(table = "`moove`", fields = f"`user-id`, `value`, `timestamp`, `channel`, `zone1`, `zone2`, {req_fields_moove}", values = f"{user_id}, 'rm', {round(time.time()) + self.dico_time['remove']}, {ctx.channel.id}, '{zone}', 'p', {req_values_moove}")
		#self.update_db(table = "`t-d-profile`", data = f'`p-soldat` = {data_p[self.dico_index_db_profile["soldat"]] + dico_value.get("soldat")}, `p-archer` = {data_p[self.dico_index_db_profile["archer"]] + dico_value.get("archer")}, `p-machine` = {data_p[self.dico_index_db_profile["machine"]] + dico_value.get("machine")}, `p-mage` = {data_p[self.dico_index_db_profile["mage"]] + dico_value.get("mage")}', condition = f'`p-id` = {user_id}')


	@commands.command()
	async def mv(self, ctx, zone1 = None, zone2 = None, *, battaillon = None):
		"""
		def checkBattaillon(message):
			return message.author == ctx.message.author and ctx.channel == message.channel and (message.content.startswith("add") or message.content.startswith("del") or message.content.startswith("go") or message.content.startswith("stop"))

		def checkEmoji(reaction, user):
			return ctx.message.author == user and msg.id == reaction.message.id and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌" or str(reaction.emoji) == "↩️")

		def checkMsg(message):
			return message.author == ctx.message.author and ctx.channel == message.channel and message.content[0].upper() in ("A", "B", "C") and message.content[1:].isdigit()
		"""
		user_id = ctx.author.id
		result = await self.verif(ctx = ctx, UserId = user_id)
		if result == False:
			return
		else:
			lang = result

		msg_del = []
		#data_p = self.select_db(table = "`t-d-profile`", fields = "*", condition = f"`p-id` = {user_id}")[0] #données du profile du joueur
		dico_value = {"soldat" : 0, "archer" : 0, "mage" : 0, "machine" : 0}

		if zone1 is None or zone2 is None:
			await ctx.send("stp renseigne les champs des zones, j'avais la flemme de faire comme pour les commandes attack, dep ou rm")
			return
		else:
			zone1 = zone1[0].upper() + zone1[1:]
			zone2 = zone2[0].upper() + zone2[1:]
			if zone1 not in self.list_zone:
				msg = await ctx.send("la zone de départ spécifiée n'existe pas")
				for m in msg_del:
					await m.delete()
				msg_del.append(msg)
				return
			if zone2 not in self.list_zone:
				msg = await ctx.send("la zone d'arrivée spécifiée n'existe pas")
				for m in msg_del:
					await m.delete()
				msg_del.append(msg)
				return
			if zone1 == zone2:
				for m in msg_del:
					await m.delete()
				msg = await ctx.send("la zone à partir de laquelle tu veux attaquer celle que tu veux attaquer sont les mêmes")
				msg_del.append(msg)
				return
			data_m1 = self.select_db(table = "`t-d-maps`", fields = "*", condition = f"`m-map` = '{zone1}'")[0]
			data_m2 = self.select_db(table = "`t-d-maps`", fields = "*", condition = f"`m-map` = '{zone2}'")[0]
			if data_m1[self.dico_index_db_maps["user_id"]] != user_id:
				await ctx.send("tu ne possèdes pas la zone1")
			if data_m2[self.dico_index_db_maps["user_id"]] != user_id:
				await ctx.send("tu ne possèdes pas la zone2")

		if battaillon is None:
			await ctx.send("stp renseigne le champs du battaillon, j'avais la flemme de faire comme pour les commandes attack, dep ou rm")
			return
		else:
			battaillon = battaillon.split(",")
			for value in battaillon:
				value = value.split()
				
				if len(value) != 2 or not value[1].isdigit() or value[0] not in ("soldat","soldats", "archer", "archers", "mage", "mages", "machine", "machines"):
					await ctx.send("syntaxe invalide dans le champs du battaillon")
					return
				if value[0] in ("soldats", "archers", "mages", "machines"):
					value[0] = value[0][:-1]
				if value[0] in dico_value: #si il y avait deja des troupes comme ca
					val = dico_value[value[0]] #on récup l'encienne valeur
					if val + int(value[1]) > data_m1[self.dico_index_db_maps[value[0]]]:
						await ctx.send(f"tu n'as pas assez d'unité en réserve. Tu ne peux ajouter que {data_m1[self.dico_index_db_maps[value[0]]] - val} {value[0]}{self.s((data_m1[self.dico_index_db_maps[value[0]]] - val))}")
						return
					dico_value[value[0]] = val + int(value[1])
		await ctx.send(f"tu as envoyé tes troupes de la zone {zone1} à la zone {zone2}")

		req_maps = ""
		req_fields_moove = ""
		req_values_moove = ""
		for value in dico_value.items():
			req_maps += f"`m-{value[0]}` = {data_m1[self.dico_index_db_maps[f'{value[0]}']] - value[1]}, "
			req_fields_moove += f"`{value[0]}`, "
			req_values_moove += f"{value[1]}, "

		req_maps = req_maps[:-2]
		req_fields_moove = req_fields_moove[:-2]
		req_values_moove = req_values_moove[:-2]

		self.update_db(table = "`t-d-maps`", data = req_maps, condition = f'`m-map` = "{zone1}"')
		self.insert_db(table = "`moove`", fields = f"`user-id`, `value`, `timestamp`, `channel`, `zone1`, `zone2`, {req_fields_moove}", values = f"{user_id}, 'mv', {round(time.time()) + self.dico_time['moove']}, {ctx.channel.id}, '{zone1}', '{zone2}', {req_values_moove}")
		#self.update_db(table = "`t-d-maps`", data = f'`m-soldat` = {data_m2[self.dico_index_db_maps["soldat"]] + dico_value.get("soldat")}, `m-archer` = {data_m2[self.dico_index_db_maps["archer"]] + dico_value.get("archer")}, `m-machine` = {data_m2[self.dico_index_db_maps["machine"]] + dico_value.get("machine")}, `m-mage` = {data_m2[self.dico_index_db_maps["mage"]] + dico_value.get("mage")}', condition = f'`m-map` = "{zone2}"')

	@commands.command()
	async def attack(self, ctx, map = None, zone1 = None, zone2 = None, *, battaillon = None):
		r"""
		msg choix de map
		   |
		   \_ wait_for emoji 20s A, B, C, D 🚫
		   |
		   | --> emoji 🚫 --> return
		   |
		msg choix zones (while True)
		   |
		   \_ wait for msg 120s 
		   |
		   | --> "stop" --> return
		   |
		   | --- verif sytaxe --> continue
				 |
				 | --> possède pas z1 --> continue
				 |
			   break
				 |        
		gestion troupe (while True)
		   |
		   \_ wait for msg 120s
		   |
		   | --> "stop" --> return
		   |
		   | --> "add"/"del"
		   |       |
		   |       | --- verif syntaxes --> continue
		   |             |
		   |             |
		   |          modif msg
		   |
		   | --> run
				|
				\_wait for ❌, ✅
				|
				| --> ❌ --> return
				|
				| --> ✅ --> lancement
		"""
		user_id = ctx.author.id
		result = await self.verif(ctx = ctx, UserId = user_id)
		if result == False:
			return
		else:
			lang = result

		def checkBattaillon(message):
			return message.author == ctx.message.author and ctx.channel == message.channel and (message.content.startswith("add") or message.content.startswith("del") or message.content.startswith("run") or message.content.startswith("stop"))

		def checkEmoji(reaction, user):
			return ctx.message.author == user and msg.id == reaction.message.id and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌" or str(reaction.emoji) == "↩️")

		def checkEmojiMap(reaction, user):
			return ctx.message.author == user and msg.id == reaction.message.id and (reaction.emoji == '🇦' or reaction.emoji == '🇧' or reaction.emoji == '🇨' or reaction.emoji == '🚫')

		def checkZone(message):
			return (message.author == ctx.message.author and ctx.channel == message.channel and message.content.split()[0].isdigit()) or message.content == "stop"

		msg_del = []
		_map = {'🇦' : "A", '🇧' : "B", '🇨' : "C"}
		dico_value = {"soldat" : 0, "archer" : 0, "mage" : 0, "machine" : 0}

		if map is not None:
			if map not in ("A", "B", "C", "a", "b", "c"):
				await ctx.send("la map spécifiée n'est pas bonne")
				return
			if map in ("a", "b", "c"):
				map = map.upper()
		else:
			msg = await ctx.send("Sur quel map voulez vous attaquer ?\n(🚫 pour stopper l'attaque)") #choix de la map
			await msg.add_reaction('🇦')
			await msg.add_reaction('🇧')
			await msg.add_reaction('🇨')
			await msg.add_reaction('🚫')

			try:
				reaction, user = await self.client.wait_for("reaction_add", timeout = 20, check = checkEmojiMap) #attente
			except:
				await ctx.send("Vous n'avez pas choisis votre map")
				for m in msg_del:
					await m.delete()
				return

			if reaction.emoji == '🚫':
				await ctx.send("attaque stoppée")
				return

			map = _map.get(reaction.emoji) #on récup la map a partir de l'emoji
		
		if zone1 is not None and zone2 is not None:
			zone1 = map + zone1
			zone2 = map + zone2
			if zone1 not in self.list_zone:
				msg = await ctx.send("la zone de départ spécifiée n'existe pas")
				for m in msg_del:
					await m.delete()
				msg_del.append(msg)
				return
			if zone2 not in self.list_zone:
				msg = await ctx.send("la zone d'arrivée spécifiée n'existe pas")
				for m in msg_del:
					await m.delete()
				msg_del.append(msg)
				return
			if zone1 == zone2:
				for m in msg_del:
					await m.delete()
				msg = await ctx.send("la zone à partir de laquelle tu veux attaquer celle que tu veux attaquer sont les mêmes")
				msg_del.append(msg)
				return

			data1 = self.select_db(table = "`t-d-maps`", fields = "*", condition = f"`m-map` = '{zone1}'")[0]
			if data1[self.dico_index_db_maps["user_id"]] != ctx.author.id:
				msg = await ctx.send("tu ne possède pas la zone de départ")
				for m in msg_del:
					await m.delete()
				msg_del.append(msg)
				return
			data2 = self.select_db(table = "`t-d-maps`", fields = "*", condition = f"`m-map` = '{zone2}'")[0]
			if data2[self.dico_index_db_maps["user_id"]] == user_id:
				await ctx.send("tu possèdes déjà la zone que tu veux attaquer")
				return
			
		elif zone1 is not None and zone2 is None:
			await ctx.send("tu n'as pas spécifié la zone d'arrivée")
			return

		else:
			while True: #choix des provinces
				#quel zone vers quel zone
				msg = await ctx.send("À partir de quel zone voulez-vous attaquer et pour aller à quel autre zone?\n(Vous pouvez aussi arrêter la commandes avec 'stop')\n\nex : `24 to 25`\nex : `3 to 6`\nex : `stop`")
				msg_del.append(msg)
				try:
					value = await self.client.wait_for("message", timeout = 120, check = checkZone)
				except:
					await ctx.send("vous n'avez pas spécifié la province que vous attaquez")
					for m in msg_del:
						await m.delete()
					return

				msg_del.append(value)


				if value.content == "stop":
					await ctx.send("Tu as stoppé l'attaque")
					for m in msg_del:
						await m.delete()
					return


				elif len(value.content.split()) == 3 and value.content.split()[0].isdigit() and value.content.split()[2].isdigit(): #si les paramètres zones sont bon
					zone1 = map+value.content.split()[0]
					zone2 = map+value.content.split()[2]
					if zone1 not in self.list_zone:
						msg = await ctx.send("la zone de départ spécifiée n'existe pas")
						for m in msg_del:
							await m.delete()
						msg_del.append(msg)
						continue
					if zone2 not in self.list_zone:
						msg = await ctx.send("la zone d'arrivée spécifiée n'existe pas")
						for m in msg_del:
							await m.delete()
						msg_del.append(msg)
						continue
					if zone1 == zone2:
						for m in msg_del:
							await m.delete()
						msg = await ctx.send("la zone à partir de laquelle tu veux attaquer celle que tu veux attaquer sont les mêmes")
						msg_del.append(msg)
						continue
					
					data1 = self.select_db(table = "`t-d-maps`", fields = "*", condition = f"`m-map` = '{zone1}'")[0]
					if data1[self.dico_index_db_maps["user_id"]] != ctx.author.id:
						msg = await ctx.send("tu ne possède pas la zone de départ")
						msg_del.append(msg)
						continue
					data2 = self.select_db(table = "`t-d-maps`", fields = "*", condition = f"`m-map` = '{zone2}'")[0]
					if data2[self.dico_index_db_maps["user_id"]] == user_id:
						await ctx.send("tu possèdes déjà la zone que tu veux attaquer")
						continue
					break



		if battaillon is not None:
			battaillon = battaillon.split(",")
			for value in battaillon:
				value = value.split()
				list_troupe = ("soldat", "soldats", "archer", "archers", "mage", "mages", "machine", "machines")
				list_troupe_s = ("soldats", "archers", "mages", "machines")
				if len(value) != 2 or value[0] not in list_troupe or not value[1].isdigit():
					await ctx.send("syntaxe invalide dans le champs du battaillon")
					return
				if value[0] in list_troupe_s:
					value[0] = value[0][:-1]
				if value[0] in dico_value: #si il y avait deja des troupes comme ca
					val = dico_value[value[0]] #on récup l'encienne valeur
					if val + int(value[1]) > data1[self.dico_index_db_maps[value[0]]]:
						await ctx.send(f"tu n'as pas assez d'unité en réserve. Tu ne peux ajouter que {data1[self.dico_index_db_maps[value[0]]] - val} {value[0]}{self.s((data1[self.dico_index_db_maps[value[0]]] - val))}")
						return
					dico_value[value[0]] = val + int(value[1])

		else:
			_msg = await ctx.send("```pa = point d'attaque\npv = point de vie\n\nsoldat : 100 de pa et 50 de pv\nmage : 100 de pa et 50 de pv\narcher : 100 de pa et 50 de pv\nmachine : 100 de pa et 50 de pv\n```")
			msgg = [] #liste des troupes qu'il ajoute au combat
			

			for v in dico_value.items():
				msgg.append(f"{v[1]} {v[0]}{self.s(v[1])} : {v[1] * self.dico_puissances[v[0]]} de puissance")
			embed = discord.Embed(description = "\n".join(msgg), title = f"**{zone1} --> {zone2}**") # + "\n\ntotaux des puissances"
			await _msg.edit(embed = embed.set_footer(text = "-add [troupe] [nombre]\n-del [troupe] [nombre]\n-stop\n-run"))



			while True: #gestion du combat
				try:
					value = await self.client.wait_for("message", timeout = 120, check = checkBattaillon) #attente d'un add, del, run, stop
				except:
					await ctx.send("tu n'as pas validé ton attaque avec le mot clé 'run'")
					for m in msg_del:
						await m.delete()
					msg_del = None
					return
				msg_del.append(value)



				if value.content.startswith("add"):
					value = value.content.split()[1:] #on récup,l'unité et le nombre
					if value[0] in ["soldat","soldats", "archer", "archers", "mage", "mages", "machine", "machines"] and value[1].isdigit(): #on vérif
						if value[0] in ["soldats", "archers", "mages", "machines"]: #on modif si nécessaire
							value[0] = value[0][:-1] #on modif si nécessaire
						if value[0] in dico_value: #si il y avait deja des troupes comme ca
							val = dico_value[value[0]] #on récup l'encienne valeur
							if val + int(value[1]) > data1[self.dico_index_db_maps[value[0]]]:
								msg_del.append(await ctx.send(f"tu n'as pas assez d'unité en réserve. Tu ne peux ajouter que {data1[self.dico_index_db_maps[value[0]]] - val} {value[0]}{self.s((data1[self.dico_index_db_maps[value[0]]] - val))}"))
								continue
							dico_value[value[0]] = val + int(value[1]) #on add et on change

						msgg = []
						for v in dico_value.items():
							msgg.append(f"{v[1]} {v[0]}{self.s(v[1])} : {v[1] * self.dico_puissances[v[0]]} de puissance")
						embed = discord.Embed(description = "\n".join(msgg), title = f"**{zone1} --> {zone2}**") # + "\n\ntotaux des puissances"
						embed.set_footer(text = "-add [troupe] [nombre]\n-del [troupe] [nombre]\n-stop\n-run")
						await _msg.edit(embed = embed)
					else:
						msg_del.append(await ctx.send("Ajout incorect (mauvaise syntaxe)\nex : `add soldat 1`"))
						continue



				elif value.content.startswith("del"):
					value = value.content.split()[1:]
					if value[0] in ["soldat", "archer", "mage", "machine"] and value[1].isdigit():
						if value[0] in ["soldats", "archers", "mages", "machines"]:
							value[0] = value[0][:-1]
						if value[0] in dico_value:
							val = dico_value[value[0]]
							if val - int(value[1]) >= 0:
								dico_value[value[0]] = val - int(value[1])
							else:
								dico_value[value[0]] = 0
							msgg = []
							for v in dico_value.items():
								msgg.append(f"{v[1]} {v[0]}{self.s(v[1])} : {v[1] * self.dico_puissances[v[0]]} de puissance")
							embed = discord.Embed(description = "\n".join(msgg), title = f"**{zone1} --> {zone2}**") # + "\n\ntotaux des puissances"
							embed.set_footer(text = "-add [troupe] [nombre]\n-del [troupe] [nombre]\n-stop\n-run")
							await _msg.edit(embed = embed)
						else:
							msg_del.append(await ctx.send("Suppression impossible (vous n'avez pas déployé ce type d'unité)."))
							continue
					else:
						msg_del.append(await ctx.send("Supression incorect (mauvaise syntaxe)\nex : `del soldat 1`"))
						continue



				elif value.content == "run":
					msg = await ctx.send("Etes vous sur d'envoyer vos troupes au combat?")
					msg_del.append(msg)
					await msg.add_reaction("✅")
					await msg.add_reaction("❌")
					await msg.add_reaction("↩️")
					try:
						reaction, user  = await self.client.wait_for("reaction_add", timeout = 20, check = checkEmoji)
					except:
						await ctx.send("tu n'as pas validé ton attaque avec la réaction ✅")
						return
					if reaction.emoji == "✅":
						await ctx.send(f"Vous avez envoyé vos troupes de la zone {zone1} vers la zone {zone2}.")
						await ctx.send("calculs et nettoyage du salon en cours...")
						for m in msg_del:
							await m.delete()
						break

					elif reaction.emoji == "↩️":
						msg_del.remove(msg)
						await msg.delete()
						continue

					else:
						await ctx.send("Vous avez anulez le combat.")
						for m in msg_del:
							await m.delete()
						msg_del = None
						return

				elif value.content == "stop": #on le supprime
					await ctx.send("Vous avez anulez le combat.")
					for m in msg_del:
						await m.delete()
					msg_del = None
					return
		
		#requetes pour editer les information de la zone de départ et faire une insertion dans la table moove
		req_maps = ""
		req_fields_moove = ""
		req_values_moove = ""
		for value in dico_value.items():
			req_maps += f"`m-{value[0]}` = {data1[self.dico_index_db_maps[f'{value[0]}']] - value[1]}, "
			req_fields_moove += f"`{value[0]}`, "
			req_values_moove += f"{value[1]}, "

		req_maps = req_maps[:-2]
		req_fields_moove = req_fields_moove[:-2]
		req_values_moove = req_values_moove[:-2]

		self.update_db(table = "`t-d-maps`", data = req_maps, condition = f"`m-map` = '{zone1}'")
		self.insert_db(table = "`moove`", fields = f"`user-id`, `value`, `timestamp`, `channel`, `zone1`, `zone2`, {req_fields_moove}", values = f"{user_id}, 'atk/0', {round(time.time()) + self.dico_time['attack']}, {ctx.channel.id}, '{zone1}', '{zone2}', {req_values_moove}")
		await ctx.send("l'attaque est lancée")

		pass






























"""
		pvp = Fight() #classe du pvp
		a = [] #listes des troupes att
		d = [] #listes des troupes def
		type_ = {"soldat" : "cac", "archer" : "dis", "mage" : "mag", "machine" : "mac"} #dico troupe : type
		dico_data_def = {"cac" : ["soldat", data2[self.dico_index_db_maps["soldat"]]], "dis" : ["archer", data2[self.dico_index_db_maps["archer"]]], "mac" : ["machine", data2[self.dico_index_db_maps["machine"]]], "mag" : ["mage", data2[self.dico_index_db_maps["mage"]]]}
		if data2[self.dico_index_db_maps["user_id"]] != 0:
			data_p = self.select_db(table = "`t-d-profile`", fields = "*", condition = f"`p-id` = {data2[self.dico_index_db_maps['user_id']]}")[0] #données du profile du défenseur
		
		req_sql_edit_map_att_if_win = ""
		for value in dico_value.items(): #dico des troupes de l'attaquant
			a = pvp.addUnits(a, self.dico_puissances[value[0]], type_[value[0]], value[0], dico_des_pv, int(value[1])) #on ajoute les troupes
			req_sql_edit_map_att_if_win += f"`m-{value[0]}` = {data1[self.dico_index_db_maps[value[0]]] - value[1]}, "
		req_sql_edit_map_att_if_win = req_sql_edit_map_att_if_win[:-2]

		for value in dico_data_def.items():
			d = pvp.addUnits(d, self.dico_puissances[value[1][0]], value[0], value[1][0], dico_des_pv, value[1][1])

		a = pvp.fight(a, d)
		l_unit_att = []
		l_unit_def = []
		dico = {True : "validée", False : "non validée", "att" : "attaquant", "def" : "défenseur"}
		for b in a["attaquant"]:
			l_unit_att.append(b.name)
		for b in a["defenseur"]:
			l_unit_def.append(b.name)
"""
#        msg_result = f"""```
#=================
#troupes restantes de l'attaquant :
#soldats : {l_unit_att.count("soldat")}
#archers : {l_unit_att.count("archer")}
#machines : {l_unit_att.count("machine")}
#mages : {l_unit_att.count("mage")}
#=================
#troupes restantes du défenseur :
#soldats : {l_unit_def.count("soldat")}
#archers : {l_unit_def.count("archer")}
#machines : {l_unit_def.count("machine")}
#mages : {l_unit_def.count("mage")}
#=================
#gagnant : {dico.get(a['winner'])}
#victoire totale : {dico.get(a['total_win'])}
#pourcentage de victoire : {a['win_percent']}%```
#        """
"""
		await ctx.send(msg_result)
		if a["winner"] == "att":
			bat = {"town" : f"{int(data2[self.dico_index_db_maps['town']].split('/')[1])}/{int(data2[self.dico_index_db_maps['town']].split('/')[2])}/{0}", "mine" : f"{int(data2[self.dico_index_db_maps['mine']].split('/')[1])}/{int(data2[self.dico_index_db_maps['mine']].split('/')[2])}/{0}", "lava_mine" : f"{int(data2[self.dico_index_db_maps['lava-mine']].split('/')[1])}/{int(data2[self.dico_index_db_maps['lava-mine']].split('/')[2])}/{0}"}
			self.update_db(table = "`t-d-maps`", data = f'`m-user` = {user_id}, `m-soldat` = {l_unit_att.count("soldat")}, `m-archer` = {l_unit_att.count("archer")}, `m-machine` = {l_unit_att.count("machine")}, `m-mage` = {l_unit_att.count("mage")}, `m-town` = "{bat.get("town")}", `m-mine` = "{bat.get("mine")}", `m-lava-mine` = "{bat.get("lava_mine")}"', condition = f'`m-map` = "{zone2}"')
			self.update_db(table = "`t-d-maps`", data = req_sql_edit_map_att_if_win, condition = f'`m-map` = "{zone1}"')
			if data2[1] != 0:
				user = self.client.get_user(data2[1])
				dm = await user.create_dm()
				try:
					await dm.send(f"Votre base en {zone2} s'est fait attaquer. Vous avez malheureusement perdu. Les unitées restantes ont été renvoyés dans votre profile.\n\n{msg_result}")
				except discord.Forbidden:
					pass
				self.update_db(table = "`t-d-profile`", data = f'`p-soldat` = {data_p[self.dico_index_db_profile["soldat"]] + l_unit_def.count("soldat")}, `p-archer` = {data_p[self.dico_index_db_profile["archer"]] + l_unit_def.count("archer")}, `p-mage` = {data_p[self.dico_index_db_profile["mage"]] + l_unit_def.count("mage")}, `p-machine` = {data_p[self.dico_index_db_profile["machine"]] + l_unit_def.count("machine")}', condition = f'`p-id` = {data2[self.dico_index_db_maps["user_id"]]}')
		else:
			self.update_db(table = "`t-d-maps`", data = f'`m-soldat` = {l_unit_def.count("soldat")}, `m-archer` = {l_unit_def.count("archer")}, `m-machine` = {l_unit_def.count("machine")}, `m-mage` = {l_unit_def.count("mage")}', condition = f'`m-map` = "{zone2}"')
			self.update_db(table = "`t-d-maps`", data = f'`m-soldat` = {datal_unit_att.count("soldat")}, `m-archer` = {l_unit_att.count("archer")}, `m-machine` = {l_unit_att.count("machine")}, `m-mage` = {l_unit_att.count("mage")}', condition = f"`m-map` = '{zone1}'")
			if data2[self.dico_index_db_maps["user_id"]] != 0:
				user = self.client.get_user(data2[self.dico_index_db_maps["user_id"]])
				dm = await user.create_dm()
				try:
					await dm.send(f"Votre base en {zone2} s'est fait attaquer. Vous avez heureusement gagné.\n\n{msg_result}")
				except discord.Forbidden:
					pass
"""
"""
	`m-town` CHAR(8), /*nombre de ferme niv1/2/3*/
	`m-mine` CHAR(8), /*nombre de mine niv1/2/3*/
	`m-lava-mine` CHAR(8) /*nombre de mine spécials niv1/2/3 (only map C)*/
"""

def setup(client):
	client.add_cog(CogPvP(client))
