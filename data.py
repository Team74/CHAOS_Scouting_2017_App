import sqlite3
import mysql.connector
import operator

class scout:
    def export(self):
        db = mysql.connector.connect(host="10.111.49.41", user="pi", passwd="pi", db="matchdat") #connect to pi
        pos = db.cursor()
        res = pos.execute('SELECT * FROM main')
        out = open('scr', 'w')
        out.write('match'+','+ 'Team'+','+ 'Team color'+','+ 'position'+','+ 'scouterName'+','+ 'Event' +','+ 'Gears'+','+ 'Miss Gears'+','+ 'High Goals'+','+ 'Miss High Goal'+','+'Low Goals'+','+ 'Capacity'+','+ 'Pick up Balls')
        out.write(','+ 'Pick up Gears' +','+ 'aHighgoal'+','+ 'aLowgoal'+','+ 'aGears'+','+ 'aCrossed'+','+ 'Climbed'+','+ 'Notes'+ '\n')
        sortedData = sorted(pos.fetchall(), key=operator.itemgetter(3,0,1))
        ha = 0
#match, team, color, position, scoutername, event, gears, miss gears, high goals, miss high goal, lowgoal, capacity, pickupball, pickupgear, ahighgoal, alowgoal, agears, acrossed, climbed, notes
        for row in sortedData:
            row7 = 'error'
            row9 = 'error'
            row13 = 'error'
            row14 = "error"
            row15 = 'error'
            row19 = 'error'

            if ((row[8]) == 1):
                row8 = 'yes'
            elif ((row[8]) == 0):
                row8 = 'no'
            if ((row[9]) == 1):
                row9 = 'yes'
            elif ((row[9]) == 0):
                row9 = 'no'
            if ((row[13]) == 1):
                row13 = 'yes'
            elif ((row[13]) == 0):
                row13 = 'no'
            if ((row[14]) == 1):
                row14 = 'yes'
            elif ((row[14]) == 0):
                row14 = 'no'
            if ((row[15]) == 1):
                row15 = 'Blue'
            elif ((row[15]) == 0):
                row15 = 'Red'
            if ((row[19]) == 1):
                row19 = 'boiler'
            elif ((row[19]) == 2):
                row19 = 'middle'
            elif ((row[19]) == 0):
                row19 = 'far'
#0,1,15,19,2,3,4,5,16,6,17,7,8,9,10,11,12,13,14,18
#8,9,13,14,15,19
            ha = ha + 1
            print ('done'+ str (ha))
            out.write(str (row[0])+',' +str (row[1])+','+ str (row15)+','+ str (row19)+','+ str (row[2])+','+ str (row[3]))
            out.write(','+ str (row[4])+','+ str (row[16])+','+ str (row[5])+','+ str (row[17])+','+ str (row[6]))
            out.write(','+ str (row[7])+','+ str (row8)+','+ str (row9)+','+ str (row[10])+','+ str (row[11])+','+ str (row[12]))
            out.write(','+ str (row13)+','+ str (row14)+','+ str (row[18])+ '\n')

        pos.close()
        db.close()

if __name__ == "__main__":
    scout().export()
