import time

import discord
from discord.ext import commands
import mysql.connector as MC

#pylint: disable=import-error
import sys
sys.path.append("../..")
import Engine.utility.functions as functions


class CogUp(commands.Cog, functions.Func):
	def __init__(self, client):
		self.client = client
		functions.Func.__init__(self, client)
		

	@commands.command() #améliore un batiment du profile
	async def up(self, ctx, bat):
		user_id = ctx.author.id
		result = await self.verif(ctx = ctx, UserId = user_id)
		if result == False:
			return
		else:
			lang = result

		if bat not in self.list_bat_profile:
			await ctx.send("le batiment rensigné n'est pas valide")
			return

		#connection, cursor = self.create_conn()
		data_p = self.select_db(table = "`t-d-profile`", fields = "*", condition = f"`p-id` = '{user_id}'")[0]
		nj = data_p[self.dico_index_db_profile["lvl"]]
		bat = self.dico_bat[bat] #get the english name of the bat
		nn = data_p[self.dico_index_db_profile[bat]] + 1
		if nn > 5:
			await ctx.send(f"ta {bat} est deja niveau maximum")
			return
		cost = self._cost(obj = bat, number = nn, lvl_player = nj)
		validation = True
		req_sql_p = ""
		for value in cost.items():
			if data_p[self.dico_index_db_profile[value[0]]] < value[1]:
				validation = False
			req_sql_p += f"`p-{value[0]}` = {data_p[self.dico_index_db_profile[value[0]]] - value[1]}, "
		if not validation:
			data = []
			for value in cost.items():
				ress_manquantes = value[1] - data_p[self.dico_index_db_profile[value[0]]]
				if ress_manquantes < 0:
					ress_manquantes = 0
				data.append(f"{value[1]} {value[0]} ({ress_manquantes} manquant(s))")
			data = '\n'.join(data)
			await ctx.send(f"pour améliorer ta {bat} niveau {nn} il te faut:\n{data}")
			return
		req_sql_p = req_sql_p[:-2]
		await ctx.send("amélioration validée")
		self.insert_db(table = "`construction`", fields = "`user-id`, `channel`, `zone`, `build`, `lvl`, `timestamp`, `people`", values = f"{user_id}, {ctx.channel.id}, 'p', '{bat}', {nn}, {round(time.time()) + self.dico_time['up'] * nn}, 0")
		self.update_db(table = "`t-d-profile`", data = req_sql_p, condition = f"`p-id` = {user_id}")


	@commands.command() #améliore un batiment d'une de ses zones    UPDATE `t-d-profile` SET `p-population` = 200, `p-gold` = 10000, `p-wood` = 5000  WHERE `p-id` = 627191994699087873;
	async def build(self, ctx, zone = None):
		def checkEmojiNum(reaction, user):
			return ctx.message.author == user and msg.id == reaction.message.id and (str(reaction.emoji) in liste_reac or str(reaction.emoji) == "<:plus:810910205453271110>")
		
		def checkAddBat(message):
			return message.author == ctx.message.author and ctx.channel == message.channel and message.content in self.list_bat



		user_id = ctx.author.id
		result = await self.verif(ctx = ctx, UserId = user_id)
		liste_reac = ["<:one:810875837863559168>", "<:two:810875881621946408>", "<:three:810875913821880350>", "<:four:810876013215088651>", "<:five:810876057229197313>", "<:six:810876102867419156>6️", "<:seven:810876171364859935>", "<:eight:810876206438023179>", "<:nine:810874232372330517>", "<:ten:810876264062779433>"]
		dico_emoji_nb = {1 : "<:one:810875837863559168>", 2 : "<:two:810875881621946408>", 3 : "<:three:810875913821880350>", 4 : "<:four:810876013215088651>", 5 : "<:five:810876057229197313>", 6 : "<:six:810876102867419156>", 7 : "<:seven:810876171364859935>", 8 : "<:eight:810876206438023179>", 9 : "<:nine:810874232372330517>", 10 : "<:ten:810876264062779433>", "max" : "<:max:833784932568006686>"}
		dico_emoji_nb_inv = {"<:max:833784932568006686>" : "max", "<:one:810875837863559168>" : 1, "<:two:810875881621946408>" : 2, "<:three:810875913821880350>" : 3, "<:four:810876013215088651>" : 4, "<:five:810876057229197313>" : 5, "<:six:810876102867419156>" : 6, "<:seven:810876171364859935>" : 7, "<:eight:810876206438023179>" : 8, "<:nine:810874232372330517>" : 9, "<:ten:810876264062779433>" : 10}
		
		#vérifications de la zone renseignée
		if result == False:
			return
		else:
			lang = result

		if zone is None:
			await ctx.send("tu n'as pas renseigné la zone")
			return
		else:
			map = zone[0]
			if map.upper() not in ("A", "B", "C"):
				await ctx.send("la zone renseignée n'existe pas")
				return
			if map in ("a", "b", "c"):
				map = map.upper()
			zone = map+zone[1:]
			if zone not in self.list_zone:
				await ctx.send("la zone renseignée n'existe pas")
				return
			data_m = self.select_db(table = "`t-d-maps`", fields = "*", condition = f"`m-map` = '{zone}'")[0]
			if data_m[self.dico_index_db_maps["user_id"]] != user_id:
				await ctx.send("la zone ne vous appartient pas")
				return
		#récupération des information des batiments sur la zone
		towns = data_m[self.dico_index_db_maps["town"]].split("/")
		mines = data_m[self.dico_index_db_maps["mine"]].split("/")
		lava_mines = data_m[self.dico_index_db_maps["lava-mine"]].split("/")
		
		"""
		if build is not None:
			if len(build.split() > 1):
				for b in build:
					if b not in ("ferme", "mine", "lava mine", "mine de lave"):
						await ctx.send("le batiment renseigné n'existe pas")
						return
					if b in ("lava mine", "mine de lave") and map != "C":
						await ctx.send("vous ne pouvez construire des mines de lave que sur la map C")
						return
			else:
				if build not in ("ferme", "mine", "lava mine", "mine de lave"):
					await ctx.send("le batiment renseigné n'existe pas")
					return
				if build in ("lava mine", "mine de lave") and map != "C":
					await ctx.send("vous ne pouvez construire des mines de lave que sur la map C")
					return
		"""
		#listage des informations de la zone avec uen association a un nombre pour chaque bat + envoie du message + envoie des réactions + wait for
		dico_bat = {}
		dico_bat_data = {"town" : towns, "mine" : mines, "lava-mine" : lava_mines}
		list_bat_max = []
		list_bat = []
		count = 1
		#constructeur qui permet d'associer un emoji a un des batiments de la zone sauf si celui ci est niveau 3.
		for bat in ("town", "mine", "lava-mine"):
			for a in range(1, 4): #1 - 2 - 3
				for _ in range(int(dico_bat_data[bat][a-1])):
					if a == 3:
						list_bat_max.append(f"- {bat} de niveau {a}  {dico_emoji_nb['max']} ")
					else:
						dico_bat[count] = [f"- {dico_emoji_nb[count]} : {bat} de niveau {a}", a, bat]
						count += 1

		town = int(towns[0]) + int(towns[1]) #on ne prend pas les batiments de niveau 3
		mine = int(mines[0]) + int(mines[1])
		lava_mine = int(lava_mines[0]) + int(lava_mines[1])
		total = town + mine + lava_mine + 1

		for a in dico_bat.items():
			list_bat.append(a[1][0])
		for a in list_bat_max:
			list_bat.append(a)
		bat = '\n'.join(list_bat)
		msg = await ctx.send(f"voici la liste de vos batiments sur la zone {zone}:\n{bat}\n\nvoici vos possibilités :\n- construire un nouveau batiment (<:plus:810910205453271110>)\n- améliorer un batiment déjà existant en cliquant sur la réaction associée au batiment")
		
		if total < 10:
			await msg.add_reaction("<:plus:810910205453271110>")

		for a in range(1, total):
			await msg.add_reaction(dico_emoji_nb[a])
		try:
			reaction, _  = await self.client.wait_for("reaction_add", timeout = 20, check = checkEmojiNum)
		except:
			await ctx.send("tu n'as pas continué ta construction")
			return

		#récupération des données du propil après avoir choisis le batiment a up / construire
		profile = self.select_db(table = "`t-d-profile`", fields = "*", condition = f"`p-id` = {user_id}")[0]
		if str(reaction.emoji) in liste_reac: #si l'emoji est dans la liste des emojis mis
			bat = dico_bat[dico_emoji_nb_inv[str(reaction.emoji)]] #bat = batiment choisis
			nn = bat[1] + 1 #nouveau niveau du batiment
			bat = bat[2] #nom du batiment

		elif str(reaction.emoji) == "<:plus:810910205453271110>":
			await ctx.send("quel type de batiment veux-tu construire (mine, mine de lave ou ferme) :")
			try:
				message = await self.client.wait_for("message", timeout = 60, check = checkAddBat)
			except:
				await ctx.send("vous n'avez pas renseigné de batiment à construire")
			nn = 1
			bat = self.dico_bat[message.content]

		nj = profile[self.dico_index_db_profile["lvl"]] #niveau du joueur
		cost = self._cost(obj = bat, number = nn, lvl_player = nj) #cout d'amélioration / fabrication
		req_sql_p = ""
		validation = True
		for value in cost.items():
			if profile[self.dico_index_db_profile[value[0]]] < value[1]:
				validation = False
			req_sql_p += f"`p-{value[0]}` = {profile[self.dico_index_db_profile[value[0]]] - value[1]}, "
		if not validation:
			data = []
			for value in cost.items():
				ress_manquantes = value[1] - profile[self.dico_index_db_profile[value[0]]]
				if ress_manquantes < 0:
					ress_manquantes = 0
				data.append(f"{value[1]} {value[0]} ({ress_manquantes} manquant(s))")
			data = '\n'.join(data)
			await ctx.send(f"pour construire ta {bat} niveau {nn} il te faut:\n{data}")
			return
		req_sql_p = req_sql_p[:-2]
			
		result = await self.validation(ctx = ctx, timeout = 20, text = "/", text_timeout = "/")
		if not result:
			await ctx.send("tu n'as pas validé ta construction")
			return
		await ctx.send("construction validée")
		self.insert_db(table = "`construction`", fields = "`user-id`, `channel`, `zone`, `build`, `lvl`, `timestamp`, `people`", values = f"{user_id}, {ctx.channel.id}, '{zone}', '{bat}', {nn}, {round(time.time()) + self.dico_time['build'] * nn}, 0")
		self.update_db(table = "`t-d-profile`", data = req_sql_p, condition = f"`p-id` = {user_id}")

	@commands.command()
	async def collect(self, ctx, zone = None, *, bat = None):
		if zone is None or bat is None:
			await ctx.send("tu n'as pas renseigé la zone ou le batiment")
			return
		user_id = ctx.author.id
		result = await self.verif(ctx = ctx, UserId = user_id)
		if result == False:
			return
		else:
			lang = result
		
		list_bat = []
		list_recompense = []
		dico_recompense = {}
		
		if zone[0].upper() not in ("A", "B", "C", "P"): #p for profile
			await ctx.send("la map renseignée n'existe pas")
			return

		if zone[0] in ("a", "b", "c", "p"):
			zone = zone[0].upper() + zone[1:]
		
		if zone not in self.list_zone and zone != "P":
			await ctx.send("la zone renseignée n'existe pas")
			return
		if zone != "P":
			data_m = list(self.select_db(table = "`t-d-maps`", fields = "*", condition = f"`m-map` = '{zone}'")[0])
			if data_m[self.dico_index_db_maps["user_id"]] != user_id and zone != "P":
				await ctx.send("la zone renseignée ne vous appartient pas")
				return
		data_p = list(self.select_db(table = "`t-d-profile`", fields = "*", condition = f"`p-id` = '{user_id}'")[0])

		if zone[0] == "P" and len(zone) != 1:
			await ctx.send("premier argumen non valide")
			return
			
		if zone == "P":
			prefix_db = "p"
			table_timestamp = "`t-d-profile`"
			condition = f"`p-id` = {user_id}"
		else:
			prefix_db = "m"
			table_timestamp = "`t-d-maps`"
			condition = f'`m-map` = "{zone}"'

		if len(bat.split(",")) > 1:
			for b in bat.split(","):
				if b[0] == " ":
					b = b[1:]
				if b not in self.list_bat:
					await ctx.send("l'un des batiments rensigné n'existe pas")
					return
				if b in self.list_bat:
					if self.dico_bat[b] not in list_bat:
						list_bat.append(self.dico_bat[b])
		elif bat in self.list_bat or bat == "*":
			if bat == "*":
				list_bat = ["mine", "town", "lava-mine"]
			elif bat in self.list_bat_mine:
				list_bat.append("mine")
			elif bat in self.list_bat_town:
				list_bat.append("town")
			elif bat in self.list_lava_mine:
				list_bat.append("lava_mine")
		else:
			await ctx.send("le batiment spécifié n'existe pas")
			return
		if zone != "P":
			dico_towns = {1 : int(data_m[self.dico_index_db_maps["town"]].split("/")[0]), 2 : int(data_m[self.dico_index_db_maps["town"]].split("/")[1]), 3 : int(data_m[self.dico_index_db_maps["town"]].split("/")[2]), 4 : 0}
			dico_mines = {1 : int(data_m[self.dico_index_db_maps["mine"]].split("/")[0]), 2 : int(data_m[self.dico_index_db_maps["mine"]].split("/")[1]), 3 : int(data_m[self.dico_index_db_maps["mine"]].split("/")[2]), 4 : 0}
			dico_lava_mines = {1 : int(data_m[self.dico_index_db_maps["lava-mine"]].split("/")[0]), 2 : int(data_m[self.dico_index_db_maps["lava-mine"]].split("/")[1]), 3 : int(data_m[self.dico_index_db_maps["lava-mine"]].split("/")[2]), 4 : 0}
		else:
			dico_towns = {1 : 0, 2 : 0, 3 : 0, 4 : 0}
			dico_towns[data_p[self.dico_index_db_profile["town"]]] = 1

			dico_mines = {1 : 0, 2 : 0, 3 : 0, 4 : 0}
			dico_mines[data_p[self.dico_index_db_profile["mine"]]] = 1

			dico_lava_mines = {1 : 0, 2 : 0, 3 : 0, 4 : 0}
			dico_lava_mines[data_p[self.dico_index_db_profile["lava-mine"]]] = 1

		req_sql_timestamp = ""
		nj = data_p[self.dico_index_db_profile["lvl"]]
		for bat in list_bat:



			if bat == "town":
				if dico_towns.get(1) + dico_towns.get(2) + dico_towns.get(3) + dico_towns.get(4) == 0:
					await ctx.send("tu ne possèdes pas de ferme sur cette zone")

				if zone != "P":
					timestamp_db = data_m[self.dico_index_db_maps['timestamp-town']]
				else:
					timestamp_db = data_p[self.dico_index_db_profile["timestamp-town"]]

				if timestamp_db > round(time.time()) and timestamp_db != 0:
					await ctx.send(f"tu ne peux récupérer tes ressources produites par ta/tes ferme que dans {timestamp_db - round(time.time())}s")
				else:
					var_s = timestamp_db - round(time.time())
					if var_s < 0:
						var_s = 300
					if var_s > 1800: #(30 minutes)
						var_s = 1800
					for town in dico_towns.items():
						for _ in range(town[1]):
							list_recompense.append(["gold", (20 * var_s / 60 * (1 + nj / 100)) ** 1+town[0]/10*2])
							list_recompense.append(["wood", (4 * var_s / 60 * (1 + nj / 100)) ** 1+town[0]/10*2])
							list_recompense.append(["food", (10 * var_s / 60 * (1 + nj / 100)) ** 1+town[0]/10*2])
							list_recompense.append(["leather", (4 * var_s / 60 * (1 + nj / 100)) ** 1+town[0]/10*2])
					req_sql_timestamp = req_sql_timestamp + f"`{prefix_db}-timestamp-town` = {round(time.time() + 300)}, "



			elif bat == "mine":
				if dico_mines.get(1) + dico_mines.get(2) + dico_mines.get(3) + dico_mines.get(4) == 0:
					await ctx.send("tu ne possèdes pas de mine sur cette zone")

				if zone != "P":
					timestamp_db = data_m[self.dico_index_db_maps['timestamp-mine']]
				else:
					timestamp_db = data_p[self.dico_index_db_profile["timestamp-mine"]]

				if timestamp_db > round(time.time()) and timestamp_db != 0:
					await ctx.send(f"tu ne peux récupérer tes ressources produites par ta/tes mine que dans {timestamp_db - round(time.time())}s")
				else:
					var_s = timestamp_db - round(time.time())
					if var_s < 0:
						var_s = 300
					if var_s > 1800: #(30 minutes)
						var_s = 1800
					for mine in dico_mines.items():
						for _ in range(mine[1]):
							list_recompense.append(["gold", (14 * var_s / 60 * (1 + nj / 100)) ** 1+mine[0]/10*2])
							list_recompense.append(["stone", (10 * var_s / 60 * (1 + nj / 100)) ** 1+mine[0]/10*2])
							list_recompense.append(["iron", (1.4 * var_s / 60 * (1 + nj / 100)) ** 1+mine[0]/10*2])
							list_recompense.append(["coal", (0.7 * var_s / 60 * (1 + nj / 100)) ** 1+mine[0]/10*2])
					req_sql_timestamp = req_sql_timestamp + f"`{prefix_db}-timestamp-mine` = {round(time.time() + 300)}, "



			elif bat == "lava-mine":
				if dico_lava_mines.get(1) + dico_lava_mines.get(2) + dico_lava_mines.get(3) + dico_lava_mines.get(4) == 0:
					await ctx.send("tu ne possèdes pas de mine de lave sur cette zone")

				if zone != "P":
					timestamp_db = data_m[self.dico_index_db_maps['timestamp-mine']]
				else:
					timestamp_db = data_p[self.dico_index_db_profile["timestamp-mine"]]

				if timestamp_db > round(time.time()) and timestamp_db != 0:
					await ctx.send(f"tu ne peux récupérer tes ressources produites par ta/tes mine de lave que dans {timestamp_db - round(time.time())}s")
				else:
					var_s = timestamp_db - round(time.time())
					if var_s < 0:
						var_s = 300
					if var_s > 1800: #(30 minutes)
						var_s = 1800
					for lava_mine in dico_lava_mines.items():
						for _ in range(lava_mine[1]):
							list_recompense.append(["lava", (0.2 * var_s / 60  * (1 + nj / 100)) ** 1+lava_mine[0]/10*2])
							list_recompense.append(["gold", (6 * var_s / 60 * (1 + nj / 100)) ** 1+lava_mine[0]/10*2])
							list_recompense.append(["iron", (0.6 * var_s / 60 * (1 + nj / 100)) ** 1+lava_mine[0]/10*2])
							list_recompense.append(["coal", (0.3 * var_s / 60 * (1 + nj / 100)) ** 1+lava_mine[0]/10*2])
					req_sql_timestamp = req_sql_timestamp + f"`{prefix_db}-timestamp-lava-mine` = {round(time.time() + 300)}, "



		for ress in list_recompense:
			if ress[0] not in dico_recompense:
				dico_recompense[ress[0]] = ress[1]
			else:
				dico_recompense[ress[0]] = dico_recompense.get(ress[0]) + ress[1]

		req_sql_profile = ""
		msg = ""
		for ress in dico_recompense.items():
			req_sql_profile = req_sql_profile + f"`p-{ress[0]}` = {round(data_p[self.dico_index_db_profile[ress[0]]] + ress[1])}, "
			msg = msg + f"\n{round(ress[1])} {ress[0]}"

		req_sql_profile = req_sql_profile[:-2]
		req_sql_timestamp = req_sql_timestamp[:-2]



		if req_sql_profile != "":
			await ctx.send(f"vous avez gagné {msg}")
			self.update_db(table = "`t-d-profile`", data = req_sql_profile, condition = f"`p-id` = {user_id}")
		if req_sql_timestamp != "":
			self.update_db(table = f"{table_timestamp}", data = req_sql_timestamp, condition = f"{condition}")
			
def setup(client):
	client.add_cog(CogUp(client))