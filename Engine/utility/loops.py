from time import time
from random import randint
import asyncio

import discord
from discord.ext import commands, tasks
import mysql.connector as MC

#pylint: disable=import-error
import sys
sys.path.append("../..")
import Engine.utility.functions as functions
from Engine.utility.fight import Fight, Troop


class Loops(commands.Cog, functions.Func):
	def __init__(self, client):
		self.client = client
		functions.Func.__init__(self, client)

	@tasks.loop(seconds = 15)
	async def _15(self):
		datas = self.select_db(table = "`moove`", fields = "*")
		for data in datas:
			if data[self.dico_index_db_moove["timestamp"]] <= round(time()):
				channel = self.client.get_channel(data[self.dico_index_db_moove["channel"]])
				if data[self.dico_index_db_moove["value"]] == "dep" or data[self.dico_index_db_moove["value"]] == "mv": #meme fonctionnement sauf pour la partie de si la zone d'arrivé ne leur appartient plus
					data_m = self.select_db(table = "`t-d-maps`", fields = "*", condition = f'`m-map` = "{data[self.dico_index_db_moove["zone2"]]}"')[0]
					if data[self.dico_index_db_moove["id"]] == data_m[self.dico_index_db_maps["user_id"]]: #si il possède encore la map
						req_map = ""
						for value in ("soldat", "archer", "machine", "mage"):
							req_map += f"`m-{value}` = {data_m[self.dico_index_db_maps[value]] + data[self.dico_index_db_moove[value]]}, "
						req_map = req_map[:-2]
						await channel.send("tes troupes sont arrivées")
						self.update_db(table = "`t-d-maps`", data = req_map, condition = f'`m-map` = "{data[self.dico_index_db_moove["zone2"]]}"')
					else: #si il ne la possède plus
						if data[self.dico_index_db_moove["value"]] == "dep": #renvoie des troupes vers le profile
							data_p = self.select_db(table = "`t-d-profile`", fields = "*", condition = f"`p-id` = {data[self.dico_index_db_moove['id']]}")[0]
							req_profile = ""
							for value in ("soldat", "archer", "machine", "mage"):
								req_profile += f"`p-{value}` = {data_p[self.dico_index_db_profile[value]] + data[self.dico_index_db_moove[value]]}, "
							req_profile = req_profile[:-2]
							await channel.send("tes troupes sont revenu dans ton profile car la zone d'arrivée ne t'appartient plus")
							self.update_db(table = "`t-d-profile`", data = req_profile, condition = f"`p-id` = {data[self.dico_index_db_moove['id']]}")
						else: #mv
							data_m = self.select_db(table = "`t-d-maps`", fields = "*", condition = f"`m-map` = '{data[self.dico_index_db_moove['zone1']]}'")[0]
							if data_m[self.dico_index_db_maps["user_id"]] == data[self.dico_index_db_moove["id"]]: #si la map de départ lui appartient toujours
								req_map = ""
								for value in ("soldat", "archer", "machine", "mage"):
									req_map += f"`m-{value}` = {data_m[self.dico_index_db_maps[value]] + data[self.dico_index_db_moove[value]]}, "
								req_map = req_map[:-2]
								await channel.send("tes troupes sont revenu sur la zone initial car la zone d'arrivée ne t'appartient plus")
								self.update_db(table = "`t-d-maps`", data = req_map, condition = f"`m-map` = '{data[self.dico_index_db_moove['zone1']]}'")
							else: #si il a perdu la zonne d'arrivée et de départ
								data_p = self.select_db(table = "`t-d-profile`", fields = "*", condition = f"`p-id` = {data[self.dico_index_db_moove['id']]}")[0]
								req_profile = ""
								for value in ("soldat", "archer", "machine", "mage"):
									req_profile += f"`p-{value}` = {data_p[self.dico_index_db_profile[value]] + data[self.dico_index_db_moove[value]]}, "
								req_profile = req_profile[:-2]
								await channel.send("la zone {} et {} ne t'appartiennent plus ainsi, tes troupes ont été renvoyées dans ton profile")
								self.update_db(table = "`t-d-profile`", data = req_profile, condition = f"`p-id` = {data[self.dico_index_db_moove['id']]}")
					self.delete_db(table = "`moove`", condition = f"`index` = {data[self.dico_index_db_moove['index']]}")

				elif data[self.dico_index_db_moove["value"]] == "rm":
					data_p = self.select_db(table = "`t-d-profile`", fields = "*", condition = f"`p-id` = {data[self.dico_index_db_moove['id']]}")[0]
					await channel.send("tu es bien récupéré tes troupes")
					req_profile = ""
					for value in ("soldat", "archer", "machine", "mage"):
						req_profile += f"`p-{value}` = {data_p[self.dico_index_db_profile[value]] + data[self.dico_index_db_moove[value]]}, "
					req_profile = req_profile[:-2]
					self.update_db(table = "`t-d-profile`", data = req_profile, condition = f"`p-id` = {data[self.dico_index_db_moove['id']]}")
					self.delete_db(table = "`moove`", condition = f"`index` = {data[self.dico_index_db_moove['index']]}")

				elif data[self.dico_index_db_moove["value"]][:3] == "atk":
					data2 = self.select_db(table = "`t-d-maps`", fields = "*", condition = f"`m-map` = '{data[self.dico_index_db_moove['zone2']]}'")[0]
					pvp = Fight()
					a = []
					d = []
					l_unit_att = []
					l_unit_def = []
					dico_data_att = {"cac" : ["soldat", data[self.dico_index_db_moove["soldat"]]], "dis" : ["archer", data[self.dico_index_db_moove["archer"]]], "mac" : ["machine", data[self.dico_index_db_moove["machine"]]], "mag" : ["mage", data[self.dico_index_db_moove["mage"]]]}
					dico_data_def = {"cac" : ["soldat", data2[self.dico_index_db_maps["soldat"]]], "dis" : ["archer", data2[self.dico_index_db_maps["archer"]]], "mac" : ["machine", data2[self.dico_index_db_maps["machine"]]], "mag" : ["mage", data2[self.dico_index_db_maps["mage"]]]}
					for value in dico_data_att.items(): #dico des troupes de l'attaquant
						a = pvp.addUnits(a, self.dico_puissances[value[1][0]], value[0], value[1][0], self.dico_pv, int(value[1][1]))

					for value in dico_data_def.items():
						d = pvp.addUnits(d, self.dico_puissances[value[1][0]], value[0], value[1][0], self.dico_pv, int(value[1][1]))

					dico = {True : "validée", False : "non validée", "att" : "attaquant", "def" : "défenseur"}

					result = pvp.fight(l_att = a, l_def = d)

					for b in result["attaquant"]:
						l_unit_att.append(b.name)
					for b in result["defenseur"]:
						l_unit_def.append(b.name)

					message_result = f"""```
=================
troupes restantes de l'attaquant :
soldats : {l_unit_att.count("soldat")}
archers : {l_unit_att.count("archer")}
machines : {l_unit_att.count("machine")}
mages : {l_unit_att.count("mage")}
=================
troupes restantes du défenseur :
soldats : {l_unit_def.count("soldat")}
archers : {l_unit_def.count("archer")}
machines : {l_unit_def.count("machine")}
mages : {l_unit_def.count("mage")}
=================
gagnant : {dico.get(result['winner'])}
victoire totale : {dico.get(result['total_win'])}
pourcentage de victoire : {result['win_percent']}%```
        """
					await channel.send(message_result)
				self.delete_db(table = "`moove`", condition = f"`index` = {data[self.dico_index_db_moove['index']]}")

	@tasks.loop(seconds = 30)
	async def _30(self):
		datas = self.select_db(table = "`construction`", fields = "*")
		for data in datas:
			if data[self.dico_index_db_construction["timestamp"]] <= round(time()):
				if data[self.dico_index_db_construction["zone"]] == "p": #profile
					self.update_db(table = "`t-d-profile`", data = f"`p-lvl-{data[self.dico_index_db_construction['build']]}` = {data[self.dico_index_db_construction['lvl']]}", condition = f"`p-id` = {data[self.dico_index_db_construction['id']]}")
				else:
					data_map = self.select_db(table = "`t-d-maps`", fields = "*", condition = f"`m-map` = '{data[self.dico_index_db_construction['zone']]}'")[0]
					if data_map[self.dico_index_db_maps["user_id"]] == data[self.dico_index_db_construction["id"]]:
						new_data = data_map[self.dico_index_db_maps[data[self.dico_index_db_construction["build"]]]].split("/")
						nn = data[self.dico_index_db_construction["lvl"]]
						if nn == 1:
							new_data[0] = str((int(new_data[0]) + 1))
						else:
							new_data[nn-2] = str((int(new_data[nn-2]) - 1))
							new_data[nn-1] = str((int(new_data[nn-1]) + 1))
						new_data = "/".join(new_data)
						self.update_db(table = "`t-d-maps`", data = f"`m-{data[self.dico_index_db_construction['build']]}` = '{new_data}'")
					else:
						#si la zone ne lui appartient plus
						pass
				channel = self.client.get_channel(data[self.dico_index_db_construction["channel"]])
				await channel.send("amélioration / construction validax")
				self.delete_db(table = "`construction`", condition = f"`index` = {data[self.dico_index_db_construction['index']]}")
		
		datas = self.select_db(table = "`ban-game`", fields = "*", condition = f"`ban` = 1")
		for data in datas:
			if data[self.dico_index_db_ban_game["timestamp"]] != 0 and data[self.dico_index_db_ban_game["timestamp"]] <= round(time()):
				self.update_db(table = "`ban-game`", data = f"`ban` = 0, `timestamp` = 0, `raise` = ''")
				await self.mp(user_id = data[self.dico_index_db_ban_game["id"]], message = "t plus ban chacal")

	@tasks.loop(seconds = 1)
	async def _1(self):
		try:
			t_d_meteor = self.select_db(table = "`t-d-meteor`", fields = "`m-meteorshower-start`, `m-meteorshower-end`, `m-arrive-meteor`, `m-leave-meteor`")
			timestamp = int(time())
			if t_d_meteor is None:
				tdp = timestamp + randint(5, 10) #timestamp debut pluie
				tfp = tdp + randint(20, 40) #timestamp fin pluie
				tdm = tdp + randint(1, 5) #timestamp debut meteor
				tfm = tdm + randint(5, 10)
				if tdp < tdm < tfm < tfp:
					self.insert_db(table = "`t-d-meteor`", fields = "`m-meteorshower-start`, `m-meteorshower-end`, `m-arrive-meteor`, `m-leave-meteor`", values = f"{tdp}, {tfp}, {tdm}, {tfm}")
			else:
				tdp, tfp, tdm, tfm = t_d_meteor[0][0], t_d_meteor[0][1], t_d_meteor[0][2], t_d_meteor[0][3]
				if timestamp >= tfp:
					tdp = timestamp + randint(5, 10) #timestamp debut pluie
					tfp = tdp + randint(20, 40) #timestamp fin pluie

					tdm = tdp + randint(1, 5) #timestamp debut meteor
					tfm = tdm + randint(5, 10) #timestamp fin meteor

					if tdp < tdm < tfm < tfp:
						self.update_db(table = "`t-d-meteor`", data = f"`m-meteorshower-start` = {tdp}, `m-meteorshower-end` = {tfp}, `m-arrive-meteor` = {tdm}, `m-leave-meteor` = {tfm}")

				if timestamp >= tfp:
					tdm = timestamp + 10 #timestamp debut meteor
					tfm = tdm + 10 #timestamp fin meteor
					if tdp < tdm < tfm < tfp:
						self.update_db(table = "`t-d-meteor`", data = f"`m-arrive-meteor`= {tdm}, `m-leave-meteor` = {tfm}")
						
		except MC.Error as err:
			print(err)

	@commands.Cog.listener()
	async def on_ready(self):
		await asyncio.sleep(1)
		#pylint: disable=no-member
		self._15.start()
		self._30.start()
		self._1.start()

def setup(client):
	client.add_cog(Loops(client))