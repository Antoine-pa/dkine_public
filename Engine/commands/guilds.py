import discord
from discord.ext import commands
import mysql.connector as MC 

#pylint: disable=import-error
import sys
sys.path.append("../..")
import Engine.utility.functions as functions

class CogGuilds(commands.Cog, functions.Func):
    def __init__(self, client):
        self.client = client
        functions.Func.__init__(client = client)
    
    @commands.command()
    async def join(self, ctx):
        pass

    @commands.command()
    async def create(self, ctx):
        pass

    @commands.command()
    async def guild(self, ctx):
        pass

def setup(client):
    client.add_cog(CogGuilds(client))