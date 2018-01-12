import sqlite3
import mysql.connector
import operator

class scout:
    def export(self):
        db = mysql.connector.connect(host="10.111.49.41", user="pi", passwd="pi", db="matchdat") #connect to pi
        pos = db.cursor()
        pos.execute('SELECT * FROM main order by round, `team color`, position')
        out = open('match', 'w')
        out.write('round'+','+ 'pos 1 red'+','+ '1R Score'+','+ 'pos 2 red'+','+ '2R Score'+','+ 'pos 3 red'+','+ '3R Score')
        out.write(','+ 'pos 1 blue'+','+ '1B Score'+','+ 'pos 2 blue' +','+ '2B Score'+','+ 'pos 3 blue'+','+ '3B Score'+','+ 'red score'+','+ 'blue score'+ '\n')
        teams = {}
        ha = 0
        self.R =   'error'
        self.RR =  'error'
        self.RRR = 'error'
        self.FR =  'error'
        self.B =   'error'
        self.BB =  'error'
        self.BBB = 'error'
        self.FB =  'error'

        for row in pos.fetchall():
            ro = row[0]
            team = row[1]
            color = row[15]
            position = row[19]
            teams.setdefault(ro,{})
            teams[ro].setdefault(color,{})
            teams[ro][color][position] = team

        '''for row in pos.fetchall():
            self.R =
            self.RR =
            self.RRR =
            self.B =
            self.BB =
            self.BBB =
            self.FR = self.R + self.RR + self.RRR
            self.FB = self.B + self.BB + self.BBB'''

        for rou ,co in teams.items():
            #print(co)
            co.setdefault(0,{})
            co[0].setdefault(0,'error')
            co[0].setdefault(1,'error')
            co[0].setdefault(2,'error')
            co.setdefault(1,{})
            co[1].setdefault(0,'error')
            co[1].setdefault(1,'error')
            co[1].setdefault(2,'error')

            out.write(str (rou)+','+str (co[0][0])+','+str (self.R)+','+str (co[0][1])+','+str (self.RR)+','+str (co[0][2])+','+str (self.RRR)+','+str (co[1][0]))
            out.write(','+str (self.B)+','+str (co[1][1])+','+str (self.BB)+','+str (co[1][2])+','+str (self.BBB)+','+str (self.FR)+','+str (self.FB)+ '\n' )

            ha = ha + 1
            print ('done'+ str (ha))

        pos.close()
        db.close()

if __name__ == "__main__":
    scout().export()
