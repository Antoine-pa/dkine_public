import discord
from discord.ext import commands
import mysql.connector as MC

#pylint: disable=import-error
import sys
sys.path.append("../..")
import Engine.utility.functions as functions

rouge = 0xCC0000 #game part

class CogMaps(commands.Cog, functions.Func):
	def __init__(self, client):
		self.client = client
		functions.Func.__init__(self, client)
		
	@commands.command(aliases = ["map"])
	async def maps(self, ctx, map = None, country = None):
		user_id = ctx.author.id
		result = await self.verif(ctx = ctx, UserId = user_id)
		if result == False:
			return
		else:
			lang = result

		if map is None and country is None:
			pass
		elif map is not None and country is None:
			if map in ["A", "B", "C"]:
				maps = self.select_db(table = "`t-d-maps`", fields = "*", condition = f'`m-map` LIKE "{map}%"')
				count = 1
				c = ""
				msg = ["```"]
				for zone in maps:
					zone = list(zone)
					if zone[1] == 0: zone[1] = "personne (vide)"
					else: zone[1] = self.client.get_user(zone[1])
					if count <= 2:
						z = f"Z{zone[0][1:]}"
						u = f"{zone[1]}"
						c = c + " |" + z + f"{' '*(3-len(z))}" + ": " + u + f"{' '*(16-len(u))}"
						count += 1
					else:
						msg.append(c)
						z = f"Z{zone[0][1:]}"
						u = f"{zone[1]}"
						c = z + f"{' '*(3-len(z))}" + ": " + u + f"{' '*(16-len(u))}"
						count = 2
				if c != "":
					msg.append(c)
				msg.append("```")
				msg[1] = msg[1][2:]
				msg = "\n".join(msg)
				embed = discord.Embed(title = f"MAP {map}", description = msg, color = rouge)
				file = discord.File(f"{self.path_dkine}/dkinebot/pictures/maps/map_{map}_net.png", filename = "map.png")
				embed.set_image(url = "attachment://map.png")
				await ctx.send(file = file, embed = embed)
		elif map is not None and country is not None:
			if not country.isdigit():
				return
			if int(country) in range(1, 34):
				zone = self.select_db(table = "`t-d-maps`", fields = "*", condition = f'`m-map` = "{map}{country}"')[0]
				if int(zone[1]) == 0:
					user = "personne"
				else:
					user = self.client.get_user(int(zone[1]))
				if user == ctx.author:
					user = "vous"
				embed = discord.Embed(title = f"zone {zone[0]}", description = f"détenteur : {user}\n\nl'image n'est pas encore disponible", color = rouge)
				embed.add_field(name = "Puissance :", value = f"puissance des soldats : {zone[2]*100}\npuissance des archers : {zone[3]*100}\npuissance des mages : {zone[4]*100}\npuissance des engins de siege : {zone[5]*100}")
				await ctx.send(embed = embed)
				
def setup(client):
	client.add_cog(CogMaps(client))
