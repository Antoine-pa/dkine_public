from time import time
from random import randint
import asyncio

import discord
from discord.ext import commands, tasks
import mysql.connector as MC
import aiohttp

import Engine.utility.functions as functions

prefix = ["!:"]
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(prefix, help_command = None, intents = intents)
token = ""
token_test = ""
bleu = 0x00FFFF
rouge = 0xCC0000
func = functions.Func(client = client)


for file in ("profile", "merdasse", "help", "periodicity", "box_meteor", "maps", "recrute", "bat", "trade", "PvP"):
	client.load_extension(f"Engine.commands.{file}")
for file in ("on_ready", "owners", "loops"):
	client.load_extension(f"Engine.utility.{file}")
#client.load_extension("skillup")


@client.command()
async def emoji(ctx, *emojis):
	print(emojis)
	


@client.event
async def on_guild_join(guild):
	try:
		func.insert_db(table = "`t-d-serv`", fields = "`s-server-id`", values = f"{guild.id}")
		nb_players = func.select_db(table = "`t-d-users`", fields = "`user-id`")
		presence = f"{len(client.guilds)} servers, {len(nb_players)} players"
		await client.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = presence))
	except MC.Error as err:
		print(err)
		
@client.event
async def on_guild_remove(guild):
	try:
		func.delete_db(table = "`t-d-serv`", condition = f"`s-server-id` = {guild.id}")
		nb_players = func.select_db(table = "`t-d-users`", fields = "`user-id`")
		presence = f"{len(client.guilds)} servers, {len(nb_players)} players"
		await client.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = presence))
	except MC.Error as err:
		print(err)

@client.event
async def on_message_edit(before, after):
	await client.process_commands(after)

@client.command()
@commands.check(func.isOwner)
async def load(ctx, file = None): #command to load cogs from a file
	if file:
		await func.del_command(ctx = ctx)
		client.load_extension(file)
		await ctx.channel.send(f"the {file} file has been loaded")
@load.error
async def load_error(ctx, error): #error management
	await func.only_owner(ctx = ctx, error = error)
	
@client.command()
@commands.check(func.isOwner)
async def unload(ctx, file = None): #command to unload cogs from a file
	if file: 
		await func.del_command(ctx = ctx)
		client.unload_extension(file)
		await ctx.channel.send(f"the {file} file has been unloaded")
@unload.error
async def unload_error(ctx, error): #error management
	await func.only_owner(ctx = ctx, error = error)
	
@client.command()
@commands.check(func.isOwner)
async def reload(ctx, file): #command to reload cogs from a file
	if file:
		await func.del_command(ctx = ctx)
		try:
			client.reload_extension(file)
			await ctx.channel.send(f"the {file} file has been reloaded")
		except:
			client.load_extension(file)
			await ctx.channel.send(f"the {file} file has been loaded")
@reload.error
async def reload_error(ctx, error): #error management
	await func.only_owner(ctx = ctx, error = error)

@client.event
async def on_command_error(ctx, error): #gestion global des erreurs
	if isinstance(error, commands.CommandNotFound):
		pass
	elif isinstance(error, commands.CheckFailure):
		pass
	elif isinstance(error, commands.MissingRequiredArgument):
		pass
	else:
		print(error)

def run():
	while True:
		try:
			client.run(token)
		except aiohttp.client_exceptions.ClientConnectorError:
			pass

run()
