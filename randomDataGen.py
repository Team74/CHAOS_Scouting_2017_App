import random as r
import mysql.connector

def ToF():
    return r.choice([1,0])

sampleTeams = [288, 74, 5444, 1762, 420, 666, 1738]

db = mysql.connector.connect(host="10.111.49.41", user="pi", passwd="pi", db="matchdat")
c = db.cursor()

def gen():
    d = list()
    d.append("Carl Best") #scouter name
    d.append(r.randint(1, 14)) #gears
    d.append(r.randint(1, 150)) #high
    d.append(r.randint(50, 500)) #low
    d.append(r.randint(5, 20)) #cap
    d.append(ToF()) #pick balls
    d.append(ToF()) #pick gears
    d.append(r.randint(1, 40)) #auton high
    d.append(r.randint(1, 60)) #auton low
    d.append(r.randint(1, 2)) #auton gears
    d.append(ToF()) #crossed
    d.append(ToF()) #climb
    d.append(ToF()) #color
    d.append(r.randint(1, 30)) #attempt gears
    d.append(r.randint(1, 40)) #high miss
    d.append("sample notes") #notes
    d.append(r.randint(1, 3)) #position
    d.append(r.choice(sampleTeams)) #team number
    d.append(r.randint(1, 100)) #round
    d.append("yeet lol") #event
    print("data:               "+str(d))
    print("team, round, event: "+str(d[-3:]))

    c.execute("SELECT * FROM `main` WHERE `team`=%s AND `round`=%s AND `event`=%s", [d[-3], d[-2], d[-1]])
    test = c.fetchone()
    if not test:
        c.execute("INSERT INTO `main`(`team`,`round`,`event`) VALUES (%s,%s,%s);", [d[-3], d[-2], d[-1]])
    else:
        print(test)

    c.execute("UPDATE `main` SET `scouterName`=%s, `gears`=%s, `highgoal`=%s, `lowgoal`=%s, `capacity`=%s, `pickupBalls`=%s, `pickupGears`=%s, `aHighgoal`=%s, `aLowgoal`=%s, `aGears`=%s, `aCrossed`=%s, `climbed`=%s, `team color`=%s, `AptGears`=%s, `MissHighGoal`=%s, `notes`=%s, `position`=%s WHERE `team`=%s AND `round`=%s AND `event`=%s;", d)
    c.execute("SELECT * FROM `main` WHERE `team`=%s AND `round`=%s AND `event`=%s", (d[-3], d[-2], d[-1]))
    print("fetchone:           "+str(c.fetchone()))
    db.commit()

for i in range(50):
    gen()

db.commit()
c.close()
db.close()
