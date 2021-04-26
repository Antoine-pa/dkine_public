import discord
from discord.ext import commands
import sys
import mysql
import mysql.connector
import asyncio
import time

prefix = ["!:", "!"]
client = commands.Bot(prefix, help_command = None)

@client.command(aliases = ["help", "h"])
async def h(message, motif):
    if motif.startswith("f"):
        msg = "**commande 1**\n`commande [arg de fdp]`\nbreve description de 3000 mots\nrepeatfor each command fdp"
        embed = discord.Embed(title= "**FIGHT**", description= msg, color= 0xCC0000)
        await message.channel.send(embed=embed)
    elif motif.startswith("e"):
                msg = "**commande 1**\n`commande [arg de fdp]`\nbreve description de 3000 mots\nrepeatfor each command fdp"
        embed = discord.Embed(title= "**ECONOMIE**", description= msg, color= 0xCC0000)
        await message.channel.send(embed=embed)            
    elif motif.startswith("fdp"):
        msg = "**commande 1**\n`commande [arg de fdp]`\nbreve description de 3000 mots\nrepeatfor each command fdp"
        embed = discord.Embed(title= "**FDP**", description= msg, color= 0xCC0000)
        await message.channel.send(embed=embed)
    else:
        msg = "**FIGHT**\n\ncommandes\n\n**ECONOMIE**\n\ncommandes\n\n**FDP**\n\ncommandes"
        embed = discord.Embed(title= "**HELP**", description=msg, color=0xCC0000)
        await message.channel.send(embed=embed)

@client.command(aliases=["link", "links"])
async def invite(message):
	msg = "Vous pouvez m'inviter dans vos serveurs avec ce lien:\nhttps://discord.com/api/oauth2/authorize?client_id=729051372628213850&permissions=8&scope=bot\n\nvous pouvez aussi rejoindre le server officiel de Dkine avec ce lien:\nhttps://discord.gg/FzJuxfV"
	await message.channel.send(msg)

client.run("NzI5MDUxMzcyNjI4MjEzODUw.XwDUAA.bQvqkKLTK8TQUCeF-VzSwFrwRF0")
