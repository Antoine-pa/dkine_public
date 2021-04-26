import discord
from discord.ext import commands
import mysql.connector as MC

import asyncio

#pylint: disable=import-error
import sys
sys.path.append("../..")
import Engine.utility.messages as messages
import Engine.utility.emote as emote

bleu = 0x00FFFF
rouge = 0xCC0000
ownerlist = [627191994699087873, 521983736485511178]


class Func(messages.Messages, emote.Emotes):
	def __init__(self, client = None):
		messages.Messages.__init__(self)
		emote.Emotes.__init__(self)
		self.client = client
		self.path_dkine = "/home/antoine/Bureau"

		self.list_unit = ("archer", "soldat", "mage", "machine")
		self.dico_puissances = {"soldat" : 100, "mage" : 100, "archer" : 100, "machine" : 100}
		self.dico_pv = 50
		self.type_ = {"soldat" : "cac", "archer" : "dis", "mage" : "mag", "machine" : "mac"} #dico troupe : type

		self.list_bat_town = ("ferme", "town")
		self.list_bat_mine = ("mine")
		self.list_lava_mine = ("lava-mine", "lava mine", "mine de lave", "mine lave", "mine-lave", "mine-de-lave")
		self.list_bat = ("ferme", "town", "mine", "lava-mine", "lava mine", "mine de lave", "mine lave", "mine-lave", "mine-de-lave")
		self.list_bat_profile = ("ferme", "town", "mine", "lava-mine", "lava mine", "mine de lave", "mine lave", "mine-lave", "mine-de-lave", "atelier", "workshop", "caserne", "barracks")
		self.dico_bat = {"ferme" : "town", "town" : "town", "mine" : "mine", "lava-mine" : "lava-mine", "lava mine" : "lava-mine", "mine de lave" : "lava-mine", "mine lave" : "lava-mine", "mine-lave" : "lava-mine", "mine-de-lave" : "lava-mine", "atelier" : "workshop", "workshop" : "workshop", "caserne" : "barracks", "barracks" : "barracks"}

		self.list_zone = ('A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28', 'A29', 'A30', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15', 'B16', 'B17', 'B18', 'B19', 'B20', 'B21', 'B22', 'B23', 'B24', 'B25', 'B26', 'B27', 'B28', 'B29', 'B30', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'C22', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30')
		self.dico_chiant = {
			"1" : ("2", "3", "4", "5", "6", "7", "8", "9"),
			"2" : ("1", "3", "8", "9", "10", "11", "26"),
			"3" : ("1", "2", "11", "12", "13", "4"),
			"4" : ("1", "3", "13", "14", "15", "5"),
			"5" : ("1", "4", "15", "16", "18", "6"),
			"6" : ("5", "1", "18", "19", "7"),
			"7" : ("1", "6", "19", "22", "24", "5"),
			"8" : ("1", "7", "24", "9", "2"),
			"9" : ("1", "8", "24", "25", "26", "2"),
			"10" : ("2", "26", "27", "28", "11"),
			"11" : ("3", "2", "10", "28", "29", "12"),
			"12" : ("13", "3", "11", "29", "30", "31", "32", "33"),
			"13" : ("14", "4", "3", "12", "33"),
			"14" : ("14", "4", "13"),
			"15" : ("17", "16", "5", "4", "14"),
			"16" : ("15", "17", "18", "5"),
			"17" : ("15", "16", "18"),
			"18" : ("17", "16", "5", "6", "19", "20"),
			"19" : ("18", "6", "7", "22", "21", "20"),
			"20" : ("19", "18", "22", "21"),
			"21" : ("20", "19", "22", "23"),
			"22" : ("21", "20", "19", "7", "24" ,"23"),
			"23" : ("21", "22", "24", "25"),
			"24" : ("25", "23", "22", "7", "8", "9"),
			"25" : ("23", "24", "9", "26"),
			"26" : ("25", "9", "2", "10", "27"),
			"27" : ("26", "10", "28"),
			"28" : ("27", "10", "11", "29"),
			"29" : ("28", "11", "12"),
			"30" : ("12", "31"),
			"31" : ("12", "30", "32", "33"),
			"32" : ("31", "33"),
			"33" : ("13", "12", "31", "32")
		}

		self.dico_table_db = {"`t-d-users`" : "dk_users", "`t-d-profile`" : "dk_users", "`ban-game`" : "dk_users", "`construction`" : "dk_users", "`t-d-timestamp`" : "dk_users", "`t-d-maps`" : "dk_maps", "`moove`" : "dk_maps", "`t-d-meteor`" : "dk_dkine", "`t-d-convois`" : "dk_dkine", "`t-d-serv`" : "dk_dkine", "`t-d-interserver-tchat`" : "dk_dkine", "`chan-lock-command`" : "dk_dkine"}
		self.dico_index_db_users = {"id" : 0, "date-creation" : 1, "lang" : 2, "ban" : 3}
		self.dico_index_db_ban_game = {"id" : 0, "ban" : 1, "raise" : 2, "timestamp" : 3, "number-ban" : 4}
		self.dico_index_db_construction = {"index" : 0, "id" : 1, "channel" : 2, "zone" : 3, "build" : 4, "lvl" : 5, "timestamp" : 6, "people" : 7}
		self.dico_index_db_profile = {"id" : 0, "premium" : 1, "population" : 2, "popu" : 2, "mood" : 3, "gold" : 4, "iron" : 5, "coal" : 6, "stone" : 7, "wood" : 8, "leather" : 9, "food" : 10, "soldat" : 11, "archer" : 12, "mage" : 13, "machine" : 14, "boat" : 15, "energy" : 16, "mine" : 17, "town" : 18, "lava-mine" : 19, "workshop" : 20, "caserne" : 21, "rep" : 22, "xp" : 23, "lvl" : 24, "meteor" : 25, "rune" : 26, "lava" : 17, "timestamp-town" : 28, "timestamp-mine" : 29, "timestamp-lava-mine" : 30}
		self.dico_index_db_timestamp = {"id" : 0, "tax" : 1, "daily" : 2, "weekly" : 3, "rep" : 4, "recrut-cac" : 5, "recrut-dist" : 6, "build-boat" : 7, "up-workshop" : 8, "regen-enery" : 9, "premium" : 10}
		self.dico_index_db_maps = {"map" : 0, "user_id" : 1, "soldat" : 2, "archer" : 3, "mage" : 4, "machine" : 5, "town" : 6, "mine" : 7, "lava-mine" : 8, "timestamp-town" : 9, "timestamp-mine" : 10, "timestamp-lava-mine" : 11}
		self.dico_index_db_moove = {"index" : 0, "id" : 1, "value" : 2, "timestamp" : 3, "channel" : 4, "zone1" : 5, "zone2" : 6, "soldat" : 7, "archer" : 8, "mage" : 9, "machine" : 10}
		self.dico_index_db_meteor = {"meteorshower-start" : 0, "meteorshower-end" : 1, "arrive-meteor" : 2, "leave-meteor" : 3}
		self.dico_index_db_convois = {"convois" : 0}
		self.dico_index_db_server = {"id" : 0}
		self.dico_index_db_tchat_inter_server = None
		self.dico_index_db_chan_lock = {"id" : 0}

		self.dico_time = {"attack" : 10, "build" : 10, "up" : 10, "moove" : 10, "remove" : 10, "dep" : 10} #in seconds

	async def verif(self, ctx, UserId, send_message = True):
		result = await self.verif_chan(ctx = ctx, send_message = send_message)
		if result == False:
			return result
		result = await self.verif_account(ctx = ctx, UserId = UserId, send_message = send_message)
		if result == False:
			return result
		lang = result
		result = await self.isBanned(ctx = ctx, UserId = UserId, send_message = send_message)
		if result == True:
			return False
		else:
			return lang
	
	async def verif_chan(self, ctx, send_message):
		data = self.select_db(table = "`chan-lock-command`", fields = "*", condition = f"`id` = {ctx.channel.id}")
		if data == []:
			return True
		if send_message:
			_ = await ctx.send("les commandes dans ce salon sont bloquées")
			#await asyncio.sleep(4)
			#await message.delete()
		return False

	async def verif_account(self, ctx, UserId, send_message):
		try:
			lang = self.select_db(table = "`t-d-users`", fields = "`user-lang`", condition = f"`user-id` = {UserId}")
			if lang == []:
				if send_message:
					await self.Embed(ctx = ctx, msg = self.msg_err_no_account.get("no-account"), color = rouge)
				return False
			else:
				return lang[0][0]
		except MC.Error as err:
				print(err)

	async def isBanned(self, ctx, UserId, send_message):
		try:
			banned = self.select_db(table = "`ban-game`", fields = "*", condition = f"`id` = {UserId}")[0]
			if banned[self.dico_index_db_ban_game["ban"]] == 1:
				if send_message:
					await self.Embed(ctx = ctx, msg = f"tu es bannis de dkine:\nraison: {banned[self.dico_index_db_ban_game['raise']]}\n\n({banned[self.dico_index_db_ban_game['number-ban']]} ban)", color = rouge)
				return True
			else:
				return False
		except MC.Error as err:
			print(err)

	#== verifs deuxieme user ==
	async def verif_recipient(self, ctx, UserId, send_message = True):
		result = await self.verif_account_recipient(ctx = ctx, UserId = UserId, send_message = send_message)
		if result == False:
			return False
		else:
			result = await self.recipientIsBanned(ctx = ctx, UserId = UserId, send_message = send_message)
			if result == True:
				return False

	async def verif_account_recipient(self, ctx, UserId, send_message):
		try:
			lang = self.select_db(table = "`t-d-users`", fields = "`user-id`", condition = f"`user-id` = {UserId}")
			if lang == []:
				if send_message:
					await self.Embed(ctx = ctx, msg = self.msg_err_no_account.get("no-account-for-recipient"), color = rouge)
				return False
		except MC.Error as err:
				print(err)

	async def recipientIsBanned(self, ctx, UserId, send_message):
		try:
			banned = self.select_db(table = "`ban-game`", fields = "*", condition = f"`id` = {UserId}")[0]
			if banned[self.dico_index_db_ban_game["ban"]] == 1:
				if send_message:
					await self.Embed(ctx = ctx, msg = f"il est banni de dkine:\nraison: {banned[self.dico_index_db_ban_game['raise']]}\n\n({banned[self.dico_index_db_ban_game['number-ban']]} ban)", color = rouge)
				return True
			else:
				return False
		except MC.Error as err:
			print(err)


	async def Embed(self, ctx, msg, color, title = None, ret = None):
		embed = discord.Embed(title = title, description = msg, color = color)
		embed.set_footer(text = ctx.author.name)
		msg = await ctx.channel.send(embed = embed)
		if ret is not None:
			return msg
	
	async def mp(self, user_id, message):
		user = self.client.get_user(user_id)
		dm = await user.create_dm()
		try:
			await dm.send(message)
		except discord.Forbidden:
			pass


	async def Logs(self, channel, embed_msg, footer_msg = False):
		chan = self.client.get_channel(channel)
		embed = discord.Embed(description = embed_msg, color = bleu)
		if footer_msg:
			embed.set_footer(text = footer_msg)
		await chan.send(embed = embed)


	def s(self, val):
		if -1 < int(val) < 1:
			return ""
		else:
			return "s"
	
	async def validation(self, ctx, timeout, text, text_timeout):

		def check(reaction, user):
			return ctx.message.author == user and message.id == reaction.message.id and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌")

		message = await ctx.send(text)
		await message.add_reaction("✅")
		await message.add_reaction("❌")

		try:
			reaction, _ = await self.client.wait_for("reaction_add", timeout = timeout, check = check)
		except:
			await ctx.send(text_timeout)
			return False
		if str(reaction.emoji) == "✅":
			return True
		else:
			return False

	async def only_owner(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.message.delete() #command deletion
			await ctx.channel.send("Seul les bot-owners ont la main sur cette commande.")

	async def del_command(self, ctx):
		await ctx.message.delete()

	def isOwner(self, ctx):
		return ctx.author.id in ownerlist
	"""truc de basdk a virer/changer/refaire
	def up_starts(self, s :str, s2: str):
		return s.upper().startswith(s2)

	async def what_ress(self, res: str, ctx):
		if res.upper().startswith("I") or res.upper().startswith("FE"):
			return "iron"
		elif res.upper().startswith("G") or res.upper().startswith("O"):
			return "gold"
		elif res.upper().startswith("C"):
			return "coal"
		elif res.upper().startswith("S") or res.upper().startswith("PI"):
			return "stone"
		elif self.up_starts(res, "W") or self.up_starts(res, "B"):
			return "wood"
		elif self.up_starts(res, "L") or self.up_starts(res, "PE"):
			return "leather"
		elif self.up_starts(res, "FO") or self.up_starts(res, "A"):
			return "food"
		else:
			await ctx.channel.send(f"{res} n'est pas une ressource connue")
			return False

	def get_level(self, xp:int):
		return int((xp/1000)**(0.5))

	async def error_message(self, ctx, err):
		await ctx.channel.send(f"Une erreure vient de survenir ||pensez a vous rendre sur le serveur support avec `!:info` pour pouvoir poser des questions et report cette erreure||.\nVoici l'erreure qui vient de survenir:{err}")
	"""
	async def number(self, ctx, value):
		if value.isdigit():
			return int(value)
		else:
			await ctx.channel.send(f"{value} n'est pas un nombre entier + faut faire le dico et l'embed")
			return False

	def create_conn(self, db):
		try:
			conn = MC.connect(host="localhost", database=f"{db}", user="dkine", password="")
			return conn, conn.cursor()
		except MC.Error as err:
				print(err)

	def select_db(self, table, fields, condition = None):
		connection, cursor = self.create_conn(self.dico_table_db[f"{table}"])
		try:
			if condition is None:
				if fields == "*":
					cursor.execute(f'SELECT {fields} FROM {table}')
				else:
					cursor.execute(f'SELECT {fields} FROM {table}')
			else:
				if fields == "*":
					cursor.execute(f'SELECT {fields} FROM {table} WHERE {condition}')
				else:
					cursor.execute(f'SELECT {fields} FROM {table} WHERE {condition}')
			return cursor.fetchall()
		except MC.Error as err:
			print(err)
		finally:
			cursor.close()
			connection.close()

	def insert_db(self, table, fields, values, condition = None):
		connection, cursor = self.create_conn(self.dico_table_db[f"{table}"])
		try:
			if condition is None:
				cursor.execute(f'INSERT INTO {table}({fields}) VALUES({values})')
			else:
				cursor.execute(f'INSERT INTO {table}({fields}) VALUES({values}) WHERE {condition}')
			connection.commit()
		except MC.Error as err:
			print(err)
		finally:
			cursor.close()
			connection.close()

	def update_db(self, table, data, condition = None):
		connection, cursor = self.create_conn(self.dico_table_db[f"{table}"])
		try:
			if condition is None:
				cursor.execute(f'UPDATE {table} SET {data}')
			else:
				cursor.execute(f'UPDATE {table} SET {data} WHERE {condition}')
			connection.commit()
		except MC.Error as err:
			print(err)
		finally:
			cursor.close()
			connection.close()

	def delete_db(self, table, condition = None):
		connection, cursor = self.create_conn(self.dico_table_db[f"{table}"])
		try:
			if condition is None:
				cursor.execute(f'DELETE FROM {table}')
			else:
				cursor.execute(f'DELETE FROM {table} WHERE {condition}')
			connection.commit()
		except MC.Error as err:
			print(err)
		finally:
			cursor.close()
			connection.close()
	
	def _cost(self, obj, number, lvl_player = None):
		cost = {}
		dico_cost = {
			"bat" : {
				"mine" : {
					"gold" : round((number*500*(1+lvl_player/100))**1.25),
					"stone" : round((number*50*(1+lvl_player/100))**1.25),
					"population" : round((number*25*(1+lvl_player/100)))},
				"town" : {
					"gold" : round((number*500*(1+lvl_player/100))**1.25),
					"wood" : round((number*100*(1+lvl_player/100))**1.25),
					"population" : round((number*25*(1+lvl_player/100)))},
				"lava-mine" : {
					"gold" : round((number*750*(1+lvl_player/100))**1.25),
					"iron" : round((number*75*(1+lvl_player/100))**1.25),
					"population" : round((number*25*(1+lvl_player/100)))},
				"workshop" : {
					"gold" : round((number*750*(1+lvl_player/100))**1.2),
					"coal" : round((number*37*(1+lvl_player/100))**1.2),
					"wood" : round((number*150*(1+lvl_player/100))**1.2),
					"population" : round((number*37*(1+lvl_player/100))**1.2)},
				"caserne" : {
					"gold" : round((number*1000*(1+lvl_player/100))**1.2),
					"stone" : round((number*100*(1+lvl_player/100))**1.2),
					"leather" : round((number*200*(1+lvl_player/100))**1.2),
					"population" : round((number*50*(1+lvl_player/100))**1.2)}
				},
			"unit" : {
				"soldat" : {"gold" : 25, "iron" : 10, "coal" : 5, "population" : 1 },
				"archer" : {"gold" : 25, "leather" : 10, "wood" : 5, "population" : 1},
				"mage" : {"gold" : 25, "leather" : 10, "rune" : 5, "popopulationpu" : 1},
				"machine" : {"gold" : 25, "wood" : 15, "stone" : 10, "population" : 2}
				}
			}
		if obj in self.list_bat_profile:
			for value in dico_cost.get("bat").get(obj).items():
				cost[value[0]] = value[1]
		elif obj in self.list_unit:
			for value in dico_cost.get("unit").get(obj).items():
				cost[value[0]] = value[1] * number
		return cost

	def _gain(self, obj, number, lvl_player):
		pass