import discord
from discord.ext import commands
import mysql.connector as MC
#"=========================================================================="
client = discord.Client
message = discord.message
list_bl = ["dc", "triche", "self", "macro", "basdk", "antoine", "dkine"]
#"=========================================================================="
#"=========================================================================="
class CogLogs(commands.Cog):
	def __init__(self, client):
		self.client = client
#"=========================================================================="
#"=========================================================================="
	async def on_message(message):
		for name in list_bl:
			if name in message.content:
				await logs_bl,send(f"{message.guild.id}{message.guild.name}\n{message.author.id}{message.author.name}\n{message.content}")
					
def setup(client):
	client.add_cog(CogLogs(client))	
