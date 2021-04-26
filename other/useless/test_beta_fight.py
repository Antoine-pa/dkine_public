#not implemented on discord
import random
import time
x_pv = 100
y_pv = 10
z_pv = 250
y_degats = 75
x_degats = 25
z_degats = 20

def qua(a, thing, count = 0):
    try:
        for item in list(a):
            if item == thing:
                count += 1
    except:
        print("ERROR")
    return count
x= "x"
y = "y"
z = "z"
a = []
b = []
cho_troop = [x, y, z]
cont= 0
while cont != 20:
    a.append(random.choice(cho_troop))
    b.append(random.choice(cho_troop))
    cont += 1
cont = 0
print(qua(b, "z"), qua(b, "x"), qua(b, "y"), qua(a, "z"), qua(a, "x"), qua(a, "y"))
tour = 0
while a != [] and b != []:
    if tour == 0:
        degats_a = qua(a, "y") * y_degats
        degats_b = qua(b, "y") * y_degats
        tour += 1
        print(degats_a, degats_b)
    else:
        tour += 1
        degats_a = qua(a, "x") * x_degats + qua(a, "z") * z_degats
        degats_b = qua(b, "x") * x_degats + qua(b, "z") * z_degats
        count = 0
        print(degats_a, degats_b)
        print(a, b)
        for item in a:
            if item == "y":
                a.pop(count)
            count += 1
        count = 0
        for item in b:
            if item == "y":
                b.pop(count)
            count += 1

    while degats_b > 0:
        try:
            rand = random.choice(a)
            if rand == "x":
                degats_b -= 100
                a.remove(rand)
            elif rand == "z" and degats_b > z_pv:
                degats_b -= 250
                a.remove(rand)
            elif rand == "z" and degats_b < z_pv:
                index = a.index("z")
                a[index] = "x"
        except:
            break
    while degats_a > 0:
        try:
            rand = random.choice(b)
            if rand == "x":
                degats_a -= 100
                b.remove(rand)
            elif rand == "z" and degats_a > z_pv:
                degats_a -= 250
                b.remove(rand)
            elif rand == "z" and degats_a < z_pv:
                index = b.index("z")
                b[index] = "x"
        except:
            break


if a == [] and b != []:
    winner = "b"
    winner_army = b
    num_x = qua(winner_army, "x")
    num_y = qua(winner_army, "y")
    num_z = qua(winner_army, "z")
if a != [] and b == []:
    winner = "a"
    winner_army = a
    num_x = qua(winner_army, "x")
    num_y = qua(winner_army, "y")
    num_z = qua(winner_army, "z")
if a == [] and b == []:
    winner = "tie"

if winner == "tie":
    print("egalitè")

else:
    print(f"le gagnant est {winner} avec {num_z} z, {num_x} x et {num_y} y ")
