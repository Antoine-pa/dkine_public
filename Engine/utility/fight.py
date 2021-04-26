import random

class Troop():
	def __init__(self, power, type_, name, life):
		self.power = power
		self.type = type_ #cac, dis, mag, mac
		self.name = name
		self.life = life
 
class Fight():
	def addUnits(self, listTroops, power, type_, name, life, number):#methode pour ajouter des troupes a une liste
		for _ in range(number):
			listTroops.append(Troop(power, type_, name, life))
		return listTroops

	def fight(self, l_att, l_def):
		#l_att -> liste d'objet Troop de l'attaquant
		#l_def -> liste d'objet Troop du défenseur

		#variables de bases
		dico_inv = {"att" : "def", "def" : "att"}
		total_puissance_att = 0
		total_puiss_end_att = 0
		_l_att = []
		list_att_cac = []
		list_att_dis = []
		list_att_mac = []
		list_att_mag = []
		dico_distrib_list_basic_att = {"cac" : list_att_cac, "dis" : list_att_dis, "mac" : list_att_mac,"mag" : list_att_mag}

		total_puissance_def = 0
		total_puiss_end_def = 0
		_l_def = []
		list_def_cac = []
		list_def_dis = []
		list_def_mac = []
		list_def_mag = []
		dico_distrib_list_basic_def = {"cac" : list_def_cac, "dis" : list_def_dis, "mac" : list_def_mac,"mag" : list_def_mag}

		total_win = False

		#distribution des unitées dans les listes
		for unit in l_att:
			unit.power *= 1 #bonus attaque global
			unit.power *= 1+random.randint(1, 5)/100
			total_puissance_att += unit.power
			dico_distrib_list_basic_att[unit.type].append(unit)
			_l_att.append(unit)

		for unit in l_def:
			unit.power *= 1.2 #bonus défense global
			unit.power *= 1+random.randint(1, 5)/100
			total_puissance_def += unit.power
			dico_distrib_list_basic_def[unit.type].append(unit)
			_l_def.append(unit)

		#dicos post construc de distrib et up des puissances / vie

		dico_troupe_globales = {"att" : l_def, "def" : l_att} #(pour moi)c bon, pas changer, c normal

		dico_fight = {
			"cac" : [{ #si le type de l'attaquant est cac
				"att" : list_att_cac, 
				"def" : list_def_cac
				}, {
				"cac" : ["p", 0, 0], #si le type de l'attaqué est cac
				"dis" : ["p", 2, 4], #si le type de l'attaqué est distance
				"mac" : ["m", 2, 4], #si le type de l'attaqué est machine
				"mag" : ["p", 1, 2] #si le type de l'attaqué est mage
			}],
			"dis" : [{ #si le type de l'attaquant est distance
				"att" : list_att_dis, 
				"def" : list_def_dis
				}, {
				"cac" : ["m", 2, 4], #si le type de l'attaqué est cac
				"dis" : ["p", 0, 0],  #si le type de l'attaqué est distance
				"mac" : ["p", 2, 4],  #si le type de l'attaqué est machine
				"mag" : ["p", 1, 2] #si le type de l'attaqué est mage
			}],
			"mac" : [{ #si le type de l'attaquant est machine
				"att" : list_att_mac, 
				"def" : list_def_mac
				}, {
				"cac" : ["p", 2, 4], #si le type de l'attaqué est cac
				"dis" : ["m", 2, 4], #si le type de l'attaqué est distance
				"mac" : ["p", 0, 0], #si le type de l'attaqué est machine
				"mag" : ["p", 1, 2] #si le type de l'attaqué est mage
			}], 
			"mag" : [{ #si le type de l'attaquant est mage
				"att" : list_att_mag, 
				"def" : list_def_mag
				}, {
				"cac" : ["p", 2, 6], #si le type de l'attaqué est cac
				"dis" : ["p", 2, 6], #si le type de l'attaqué est distance
				"mac" : ["p", 2, 6], #si le type de l'attaqué est machine
				"mag" : ["p", 0, 0] #si le type de l'attaqué est mage
			}]
		}
		

		#combat
		while True:
			for _type in ("mac", "mag", "dis", "mag", "cac"):
				for player in ("att", "def"):
					for unit in dico_fight.get(_type)[0].get(player): #return la liste de troupe du moment qui attaque
						if len(l_att) == 0 or len(l_def) == 0: #si l'une des deux équipe est décimée
							if len(l_att) == 0: #si le défenseur a gagné
								#calculs de puissance restante chez le défenseur et son pourcentage
								for unit in l_def:
									total_puiss_end_def += unit.power
								percent_puiss_end_def = round(total_puiss_end_def * 100 / total_puissance_def)

								#calculs des troupes restantes
								if percent_puiss_end_def > 75: #si il reste plus de 40% de la puissance de départ au défenseur
									_l_att = [] #l'attaquan s'esr fait éclater
									total_win = True #total win de du défenseur
								else: #si il lui reste moins de 40%
									for unit in _l_att: #on parcours les unitées de base de l'attaquant
										nb = random.randint(0, 100)
										if nb > (percent_puiss_end_def / 3): #si il a pas de chance
											_l_att.remove(unit) #on retire des unitées de l'attaque
								_l_def = l_def
								percent_win = percent_puiss_end_def
								winner = "def"


							if len(l_def) == 0: #si l'attaquant a gagné
								#calculs de puissance restante chez l'attaquant et son pourcentage
								for unit in l_att:
									total_puiss_end_att += unit.power
								percent_puiss_end_att = round(total_puiss_end_att * 100 / total_puissance_att)

								#calculs des troupes restantes
								if percent_puiss_end_att > 75: #si il reste plus de 40% de la puissance de départ à l'attaquant
									_l_def = [] #le défenseur s'esr fait éclater
									total_win = True #total win de l'attaquant
								else: #si il lui reste moins de 40%
									for unit in _l_def: #on parcours les unitées de base du défenseur
										nb = random.randint(0, 100)
										if nb > (percent_puiss_end_att / 3): #si il a pas de chance
											_l_def.remove(unit) #on retire des unitées de la défense
								_l_att = l_att
								percent_win = percent_puiss_end_att
								winner = "att"
							return {"winner" : winner, "total_win" : total_win, "attaquant" : _l_att, "defenseur" : _l_def, "win_percent" : percent_win}


						unit_att = random.choice(dico_troupe_globales.get(player)) #choisis au hasard dans la liste de troupe adverse
						list_ = dico_fight.get(_type)[1].get(unit_att.type)
						if list_[0] == "p":
							unit_att.life = unit_att.life - round(unit.power / 150 + random.randint(list_[1], list_[2])/50, 2)
						else:
							unit_att.life = unit_att.life - round(unit.power / 150 - random.randint(list_[1], list_[2])/50, 2)
						if unit_att.life <= 0:
							dico_fight.get(unit_att.type)[0].get(dico_inv.get(player)).remove(unit_att)
							dico_troupe_globales.get(player).remove(unit_att)


"""
machine   --> soldat
soldat    --> archer
archer    --> machine
"""
