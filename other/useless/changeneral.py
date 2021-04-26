import discord
from discord.ext import commands
import mysql.connector as MC
#"=========================================================================="
prefix = "!:"
client = commands.Bot(prefix, help_command = None)
#"=========================================================================="
rouge = 0xCC0000 #partie jeu
vert = 0x00CC00 #partie confirmation
bleu = 0x00FFFF #partie modération
marron = 0x582900 #partie tchat général
#"=========================================================================="
class CogTchatInterserver(commands.Cog):
    def __init__(self, client):
        self.client = client
#"=========================================================================="
    @client.command()
    async def general(self, ctx):
        try:
            connection = MC.connect(host = 'localhost', database = 'dkinedata', user = 'root', password = '')
            cursor = connection.cursor()
            cursor.execute('SELECT `it-id` FROM `t-d-interserver-tchat`')
            table_interserver_tchat = cursor.fetchall()

            if ctx.channel.id in table_interserver_tchat:
                await ctx.channel.send("Ce salon fait déjà partis des salons du tchat interserveur")
            else:
                cursor.execute(f'INSERT INTO `t-d-interserver-tchat`(`it-id`) VALUES({ctx.channel.id})')
                connection.commit()
                await ctx.channel.send("Ce salon fait désormais partis du tchat interserveur.")
        except MC.Error as err:
            print(err)
        finally:
            cursor.close()
            connection.close()
#"=========================================================================="
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == False:
            try:
                connection = MC.connect(host = 'localhost', database = 'dkinedata', user = 'root', password = '')
                cursor = connection.cursor()
                cursor.execute('SELECT `it-id` FROM `t-d-interserver-tchat`')
                table_interserver_tchat = cursor.fetchall()
                chan_id = (message.channel.id, ) #recup de l'id du channel où il y a le message
                if chan_id in table_interserver_tchat:
                    chan_id = chan_id[0]
                    for it_id in table_interserver_tchat:
                        it_id = it_id[0]
                        if chan_id != it_id:
                            embed = discord.Embed(title = f"__**`{message.author.name}`**__ :", description = f"\n{message.content}", color = marron)
                            channel = self.client.get_channel(int(it_id)) #le salon dans lequel le msg doit etre send
                            await channel.send(embed = embed)
            except MC.Error as err:
                print(err)
            finally:
                cursor.close()
                connection.close()
#"=========================================================================="
def setup(client):
    client.add_cog(CogTchatInterserver(client))