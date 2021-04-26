import discord
from discord.ext import commands
import mysql.connector as MC
from PIL import Image, ImageDraw, ImageFont

import fonction

class CogSkillup(commands.Cog, fonction.Func):
    def __init__(self, client):
        fonction.Func.__init__(self, client)
        self.client = client
        
    @commands.command()
    async def skillup(self, ctx, skill = None):
        if skill is None:
            rep = self.select_db(table = "`t-d-profile`", fields = "`p-rep`", condition = f"`p-id` = 627191994699087873")[0][0]
            
            dict_1 = {
                "1.1":([100, 0, 0, 0, 0], "cac boost", "+10%"), 
                "1.2":([50, 50, 0, 0, 0], "new troop", "troop x")
            }

            dict_2 = {
                "2.1":([100, 50, 0, 0, 0], "new bat", "batiment y"),
                "2.2":([50, 50, 200, 0, 0], "bat speed boost", "10%")
            }

            dict_3 = {
                "3.1":([400, 30, 20, 0, 0], "prod", "+10%"),
                "3.2":([40, 200, 50, 100, 0], "new thing", "jspquoi")
            }


            points = {
                "fr" : f"points de réputation:{rep}",
                "en" : f"recovery points:{rep}",
                "it" : f"punto di reputazione:{rep}"
            }

            im = Image.open("/home/antoine/Bureau/dkinebot/skillup_dkine.png")
            font = ImageFont.truetype("/home/antoine/Bureau/dkinebot/cour.ttf", 25, )
            draw = ImageDraw.Draw(im)
            draw.text((38, 107), points.get("fr"), (0, 0, 0), font = font)
            im.save("/home/antoine/Bureau/dkinebot/image.png", "PNG")
            await ctx.channel.send(file = discord.File("/home/antoine/Bureau/dkinebot/image.png"))
            
def setup(client):
    client.add_cog(CogSkillup(client))