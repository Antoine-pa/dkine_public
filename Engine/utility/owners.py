import discord
from discord.ext import commands
import mysql.connector as MC

import io
import contextlib
import textwrap
import traceback
import os
import inspect
import time

#pylint: disable=import-error
import sys
sys.path.append("../..")
import Engine.utility.functions as functions
#pylint: enable=import-error

bleu = 0x00FFFF
rouge = 0xCC0000
ownerlist = [627191994699087873, 521983736485511178]

class OldVar:
	def __init__(self):
		self.dico_var = {}
	
	def set(self, name, value):
		self.dico_var[name] = value

Vars = OldVar()

def isOwner(ctx):
	return ctx.author.id in ownerlist

class CogOwners(commands.Cog, functions.Func):
	def __init__(self, client):
		self.client = client
		functions.Func.__init__(self, client)
		
	@commands.command()
	@commands.check(isOwner)
	async def dep_account(self, ctx, id1, to, id2):
		try:
			self.update_db(table = "`t-d-users`", data = f"`user-id` = {id2}", condition = f"`user-id` = {id1}")
			self.update_db(table = "`t-d-profile`", data = f"`p-id` = {id2}", condition = f"`p-id` = {id1}")
			self.update_db(table = "`t-d-tmestamp`", data = f"`t-user-id` = {id2}", condition = f"`t-user-id` = {id1}")
			result = self.select_db(table = "`t-d-maps`", fields = "*", condition = f"m-user = {id1}")
			if result != []:
				for field in result:
					self.update_db(table = "`t-d-maps`", data = f"`m-user` = {id2}", condition = f'`m-map` = "{field[0]}"')
		except MC.Error as err:
			print(err)
			
	@commands.command()
	@commands.check(isOwner)
	async def bye(self, ctx, *, raison = "Test de commande."):
		await self.del_command(ctx = ctx)
		await self.Logs(channel = 747073930547691551, embed_msg = f"`bot off`\nRaison : {raison}")
		await self.Embed(ctx = ctx, msg = "Bye owner I'm go to bed.", color = rouge)
		self.client.close()
	@bye.error
	async def bye_error(self, ctx, error): #error management
		await self.only_owner(ctx = ctx, error = error)
		
	@commands.command()
	@commands.check(isOwner)
	async def add_premium(self, ctx, id, duration):
		try:
			premium = self.select_db(table = "`t-d-profile`", fields = "`p-premium`", condition = f"`p-id`= {id}")[0][0]
			if premium == 0:
				self.update_db(table = "`t-d-timestamp`", data = f"`t-premium` = {duration}", condition = f"`t-user-id` = {id}")
				self.update_db(table = "`t-d-profile`", data = "`p-premium` = TRUE", condition = f"`p-id` = {id}")
				await self.Embed(ctx, msg = f"mtn il a un premium de {duration}", color = rouge)
			else:
				seconds = self.select_db(table = "`t-d-timestamp`", fields = "`t-premium`", condition = f"`t-user-id`= {id}")[0][0]
				minutes = seconds // 60
				seconds %= 60
				hours = minutes // 60
				minutes %= 60
				days = hours // 24
				hours %= 24
				await self.Embed(ctx, msg = f"Il lui reste un premium de {days}j{hours}h{minutes}min{seconds}s\n[en_msg]\n[it_msg]", color = rouge)
		except MC.Error as err:
			print(err)
			
	@commands.command()
	@commands.check(isOwner)
	async def remove_premium(self, ctx, id):
		try:
			premium = self.select_db(table = "`t-d-profile`", fields = "`p-premium`", condition = f"`p-id`= {id}")[0][0]
			if premium == 1:
				seconds = self.select_db(table = "`t-d-timestamp`", fields = "`t-premium`", condition = f"`t-user-id`= {id}")[0][0]
				self.update_db(table = "`t-d-timestamp`", data = "`t-premium` = NULL", condition = f"`t-user-id` = {id}")
				self.update_db(table = "`t-d-profile`", data = "`p-premium` = FALSE", condition = f"`p-id` = {id}")
				minutes = seconds // 60
				seconds %= 60
				hours = minutes // 60
				minutes %= 60
				days = hours // 24
				hours %= 24
				await self.Embed(ctx, msg = f"Il lui restait un premium de {days}j{hours}h{minutes}min{seconds}s\n[en_msg]\n[it_msg]", color = rouge)
			else:
				await self.Embed(ctx, msg = "Il n'avais pas de premium\n[en_msg]\n[it_msg]", color = rouge)
		except MC.Error as err:
			print(err)


	def clean_code(self, code):
		shell = False
		one_line = False
		if "--print " in code:
			shell = True
			code = code.replace("--print ", "")
		elif "-p " in code:
			shell = True
			code = code.replace("-p ", "")
		code = code.split("\n")
		if code[0].startswith("```"):
			code = code[1:]
		if code[-1].startswith("```"):
			code = code[:-1]
		if len(code) == 1:
			if "=" not in code[0]:
				one_line = True
		code = "\n".join(code)
		return code, shell, one_line

	def clean_output(self, output):
		lvl_indent = 0
		var = ""
		space = False
		for a in output:
			if a in ("[", "{", "("):
				lvl_indent += 1
				var += a + "\n" + "    " * lvl_indent
			elif a in ("]", "}", ")"):
				lvl_indent -= 1
				var += "\n" + "    " * lvl_indent + a
			elif a == ",": var += ",\n" + "    " * lvl_indent
			elif a in ("'", '"'):
				if space: space = False
				else: space = True
				var += a
			elif a == " ":
				if space: var += a
			else: var += a
		return var

	@commands.command()
	@commands.check(isOwner)
	async def _eval(self, ctx, *, code):
		local_variables = {
			"commands" : commands,
			"client" : self.client,
			"discord" : discord,
			"func" : functions.Func(client = self.client),
			"ctx" : ctx,
			"sql" : MC,
			"MC" : MC,
			"mc" : MC,
			"code" : code,
			"os" : os,
			"imp" : __import__
		}
		for value in Vars.dico_var.items():
			local_variables[value[0]] = value[1]
		code, shell, one_line = self.clean_code(code)
		buffer = io.StringIO()
		result = f"Input :\n```py\n{code}\n```"
		ret = ""
		try:
			with contextlib.redirect_stdout(buffer):
				if one_line:
					output = eval(code, local_variables)
					if output is None:
						output = ""
					output = self.clean_output(str(output) + "\n" + buffer.getvalue())
				else:
					exec(f"async def _func():\n{textwrap.indent(code, '	')}", local_variables)
					#pylint: disable=not-callable
					ret = await local_variables["_func"]()
					#pylint: enable=not-callable
					if ret is not None:
						ret = f"\nreturn :\n```\n{ret}```"
					else:
						ret = ""
					if buffer.getvalue() == "":
						output = "/"
					else:
						output = self.clean_output(buffer.getvalue())
				result += f"\nOutput :\n```\n{output}\n```" + ret
			if shell:
				print(output)
			_vars = local_variables.get("code", "").split("\n")
			for var in _vars:
				var = var.split(" = ")
				if len(var) > 1:
					if var[1][0] in ("'", '"') and var[1][-1] in ("'", '"'):
						var[1] = var[1][1:-1]
					try:
						Vars.set(var[0], eval(var[1], local_variables))
					except:
						result += f"""\nan error occured"""
		except:
			result += f"""\nerror :\n```\n{traceback.format_exc()}```\n"""
		finally:
			await self.Embed(ctx = ctx, msg = result, color = 0xCC0000, title = "EVAL")

	
	@commands.command(aliases = ["sida"])
	@commands.check(isOwner)
	async def ban_game(self, ctx, id:int, number:int = 1, indic:str = "i", *,raison = ""):
		result = await self.verif_account(ctx = ctx, UserId = id, send_message = False)
		time_add = round(time.time())
		if not result:
			await ctx.send("la personne a bannir n'a pas de compte")
			return
		lang = result
		result = await self.isBanned(ctx = ctx, UserId = id, send_message = False)
		data = self.select_db(table = "`ban-game`", fields = "*", condition = f"`id` = {id}")[0]
		if result == True:
			result = await self.validation(ctx, timeout = 20, text = "la personne est déja banni. Veux tu lui rajouter le temps indiqué?", text_timeout = "tu n'as pas validé")
			if not result:
				await ctx.send("tu as annulé la commande")
				return
			else:
				old_timestamp = data[self.dico_index_db_ban_game["timestamp"]]
				if old_timestamp == 0:
					await ctx.send()
					result = await self.validation(ctx = ctx, timeout = 20, text = "son ban est de durée infini. voulez vous le remplacer?", text_timeout = "tu n'as pas validé")
					if not result:
						await ctx.send("tu as annulé la commande")
						return
				else:
					time_add = data[self.dico_index_db_ban_game["timestamp"]]


		list_indic = ("i", "s", "min", "h", "d", "w", "m")
		if indic not in list_indic:
			await ctx.send("la durée rensignée n'existe pas")
		dico_indic_time_ban = {"i" : 0, "s" : number * 1 + time_add, "min" : number * 60 + time_add, "h" : number * 3600 + time_add, "d" : number * 86400 + time_add, "w" : number * 604800 + time_add, "m" : number * 18144000 + time_add}
		self.update_db(table = "`ban-game`", data = f"`ban` = 1, `timestamp` = {dico_indic_time_ban[indic]}, `number-ban` = {data[self.dico_index_db_ban_game['number-ban']] + 1}", condition = f"`id` = {id}")
		await ctx.channel.send(f"le joueur {self.client.get_user(id)} as été banni ({data[self.dico_index_db_ban_game['number-ban']] + 1}) ban\nraison:\n{raison}\n\n{dico_indic_time_ban[indic] - round(time.time())}s")
		await self.mp(user_id = id, message = "t ban")
	@commands.command()
	@commands.check(isOwner)
	async def unban_game(self, ctx, id:int):
		result = await self.verif_account(ctx = ctx, UserId = id, send_message = False)
		if not result:
			await ctx.send("la personne a unban n'a pas de compte")
			return
		lang = result
		result = await self.isBanned(ctx = ctx, UserId = id, send_message = False)
		if not result:
			await ctx.send("il est pas ban")
		data = self.select_db(table = "`ban-game`", fields = "*", condition = f"`id` = {id}")[0]
		self.update_db(table = "`ban-game`", data = "`ban` = 0, `timestamp` = 0, `raise` = ''", condition = f"`id` = {id}")
		await ctx.send(f"tu as unban {self.client.get_user(id)}")
		await self.mp(user_id = id, message = "t'es unban")
	
	@commands.command()
	@commands.check(isOwner)
	async def ban_info(self, ctx, id:int):
		result = await self.verif_account(ctx = ctx, UserId = id, send_message = False)
		if not result:
			await ctx.send("la personne a unban n'a pas de compte")
			return
		lang = result
		result = await self.isBanned(ctx = ctx, UserId = id, send_message = False)
		if not result:
			await ctx.send("il est pas ban")
		data = self.select_db(table = "`ban-game`", fields = "*", condition = f"`id` = {id}")[0]
		await ctx.send(f"user:\n{self.client.get_user(id)}\n\nraison du ban:\n{data[self.dico_index_db_ban_game['raise']]}\n\ndurée restante:\n{data[self.dico_index_db_ban_game['timestamp']] - round(time.time())}s\n\nnombre de ban:\n{data[self.dico_index_db_ban_game['number-ban']]}")

"""
	@commands.command()
	@commands.check(isOwner)
	async def set_valor(ctx, user_id, ressource, valor, add = False):
		await self.del_command(ctx = ctx)
		connection, cursor = self.create_conn()
		try:
			actual_valor = cursor.execute(f"SELECT `p-{ressource}` FROM `t-d-profile` WHERE `p-id` = {user_id}")
			new_valor = actual_valor * int(add) + valor
			cursor.execute(f"UPDATE `p-profile` WHERE `p-id` = {user_id} SET `p-{ressource}` = {new_valor}")
			connection.commit()
			await ctx.channel.send(f"Les changements a la personne {client.user(user_id)} ont été correctement effecté")
		except:
			await ctx.channel.send("Une erreur vient de se reproduire")
		finally:
				cursor.close()
				connection.close()
	@set_valor.error
	async def set_valor_error(self, ctx, error): #error management
		await self.only_owner(ctx = ctx, error = error)
"""

def setup(client):
	client.add_cog(CogOwners(client))
