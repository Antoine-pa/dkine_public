
class Messages:
	def __init__(self):
		

		self.help_msg = {
			"fr_menu" : "Bienvenue sur le menu d'aide.\n\nVoici les catégories de commande:\n\n> `!:help profile`\n> `!:help resources`",
			"fr_profile" : "Votre profile est votre inventaire de jeu (votre compte).\nVous pourrez ouvrir votre profile grâce à la commande `!:profile`. Vous verrez alors vos ressources aparaître.\n\nFais la commande `!:help resources` pour avoir plus d'information.",
			"fr_resources" : "Votre empire possède un grand nombre de ressource. Elles vous permetteront d'effectuer certaines action et c'est ce qu'on va voir si-dessous:\n\n\n>la population : c'est votre indicateur pour connaître votre population\n\n>l'humeur : c'est l'indicateur de joie de la population. Il est influencé par les taxes notament\n\n>les minéraux : vous pouvez récuperer des minéraux dans les mines. Ils vous servront notament pour la fabrication/amélioration.\n\n>les autres ressources : vous pourrez les avoir dans les fermes. ils vous servirioons notamment à nourrir votre population ou fabriquer des choses\n\n>la partie militaire : elle vous indiquera le nombre de troupe, votre puissance ou encore votre énergie pour les déplacement de troupe.\n\n>les bâtiments : c'est votre nombre de ferme, de mine et votre niveau d'atelier.",
			"fr_"

			"en_menu" : "",
			"en_profile" : "",
			"en_resources" : "",

			"it_menu" : "",
			"it_profile" : "",
			"it_resources" : ""
			}

		self.info_msg = {
			"fr_msg" : "- Créateurs : \n- Designer : \n- Langage : python, mysql\n- Module : discord.py\n- Date lancement du projet : \n- Date de sortie : \n\nRemerciement :\nMerci à Electro qui nous héberge dkine pour un prix plus que concurentiel, merci à Jules, Mine, Snip et j'en passe de m'avoir soutenu et cru dans le projet, merci a basdk qui m'a permis de me lancer dans la conception de ce jeu et qui n'a malheureusement pas pu continuer de le dev avec moi. Merci a tout les autres dont je ne peux citer le nom car il y en a trop :) merci à tous!!!",
			
			"en_msg" : "",
			
			"it_msg" : ""
			}
			
		self.msg_err_no_account = {
			"no-account" : "Tu n'as aucun compte attribué.\n[en message]\n[it message]\n\nFais la commande `!:start` pour t'en faire un.\n[en message]\n[it message]\n\nSi tu rencontre un probleme, n'hésite pas a te tourner vers le support sur le serveur officiel que tu peux rejoindre via la commande `!:invite`\n[en message]\n[it message]",
			"no-account-for-recipient" : "Le destinataire ne possède pas de compte.\n[en message]\n[it message]\n\nCe dernier doit faire la commande `!:start` pour s'en faire un.\n[en message]\n[it message]"
			}

		self.msg_ban = {
			"fr-ban" : "Tu es bannis du jeu dkine.",
			"en-ban" : "",
			"it-ban" : ""
			}
"""
import discord
from discord.ext import commands
"""
"""
@commands.command()
async def info(ctx):
	lang = "fr"
	await ctx.send(info_msg.get(f"{lang}_msg"))
"""
