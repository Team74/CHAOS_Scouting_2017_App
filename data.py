import sqlite3
import mysql.connector
import operator

class scout:
    def export(self):
        db = mysql.connector.connect(host="10.111.49.41", user="pi", passwd="pi", db="matchdat") #connect to pi
        pos = db.cursor()
        res = pos.execute('SELECT * FROM main')
        out = open('scr', 'w')
        out.write('Round'+','+ 'Team'+','+ 'scouterName'+','+'Event' +','+ 'Gears'+','+ 'High Goals'+','+ 'Low Goals'+','+ 'Capacity'+','+ 'Pick up Balls')
        out.write(','+ 'Pick up Gears' +','+ 'aHighgoal'+','+ 'aLowgoal'+','+ 'aGears'+','+ 'aCrossed'+','+ 'Climbed'+ '\n')
        sortedData = sorted(pos.fetchall(), key=operator.itemgetter(3,0,1))

        for row in sortedData:
            row7 = 'error'
            row9 = 'error'
            row13 = 'error'
            row14 = "error"

            if ((row[7]) == 1):
                row7 = 'yes'
            elif ((row[7]) == 0):
                row7 = 'no'
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

            print (str (row[1])+','+ str (row[0])+','+ str (row7)+','+ str (row9)+','+ str (row13) +','+ str (row14))
            out.write(str (row[0])+',' +str (row[1])+','+ str (row[2])+','+ str (row[3])+','+ str (row[4])+','+ str (row[5])+','+ str (row[6]))
            out.write(','+ str (row7)+','+ str (row[8])+','+ str (row9)+','+ str (row[10])+','+ str (row[11])+','+ str (row[12]))
            out.write(','+ str (row13)+','+ str (row14)+','+ '\n')

        pos.close()
        db.close()

if __name__ == "__main__":
    scout().export()
