import discord
from discord.ext import commands, tasks
token_test = ""
intents = discord.Intents.default()
intents.members = True
prefix = "!!"
client = commands.Bot(prefix, help_command = None, intents = intents)
@client.command()
async def emoji(ctx, *emojis):
    for e in emojis:
        print(e)

@client.event
async def on_message(message):
    print(message.content)
    await client.process_commands(message)
    
client.run(token_test)
