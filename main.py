from kivy.app import App
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import BorderImage
from kivy.properties import *
from kivy.lang import Builder

from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

import signal
import sys
import threading
import sqlite3
import mysql.connector
import time
import os
import random
import string

CURRENT_EVENT = "Worlds"

piip = "10.111.49.62"

DEBUG = 1
def debug(msg, type="normal"):
    if DEBUG:
        msg = list(str(msg))
        if type == "title":
            for i in range(5):
                msg.insert(0, "-")
                msg.append("-")
        if type == "header":
            msg.insert(0, "-")
            for i in range(2):
                msg.insert(0, " ")
        if type == "header 2":
            msg.insert(0, "  ")
        msg = "".join(msg)
        print("[hol up ] [debug       ]" + msg)

#UI color settings
Builder.load_string("""
<cLabel>:
    canvas.before:
        BorderImage:
            source: "/colors/background.jpg"
            pos: self.x - 1, self.y - 1
            size: self.width + 2, self.height + 2
        Color:
            rgb: self.rgb
        Rectangle:
            pos: self.pos
            size: self.size

<cButton>:
    background_normal: ""
    background_color: self.rgb
    canvas.before:
        BorderImage:
            source: "/colors/background.jpg"
            pos: self.x - 1, self.y - 1
            size: self.width + 2, self.height + 2

#:kivy 1.0.9

<PongBall>:
    size: 50, 50
    canvas:
        Ellipse:
            pos: self.pos
            size: self.size

<PongPaddle>:
    size: 64, 200
    canvas:
        Rectangle:
            pos:self.pos
            size:self.size

<PongGame>:
    ball: pong_ball
    player1: player_left
    player2: player_right

    canvas:
        Rectangle:
            pos: self.center_x-5, 0
            size: 10, self.height

    Label:
        font_size: 70
        center_x: root.width / 4
        top: root.top - 50
        text: str(root.player1.score)

    Label:
        font_size: 70
        center_x: root.width * 3 / 4
        top: root.top - 50
        text: str(root.player2.score)

    PongBall:
        id: pong_ball
        center: self.parent.center

    PongPaddle:
        id: player_left
        x: root.x
        center_y: root.center_y

    PongPaddle:
        id: player_right
        x: root.width-self.width
        center_y: root.center_y
""")

#Overwriting normal widget classes to make them pretty
class cLabel(Label):
    def __init__(self, rgb=[0.5,0.5,0.5], **kwargs):
        self.rgb = rgb + [1]
        super(cLabel, self).__init__(**kwargs)
class cButton(Button):
    def __init__(self, rgb=[0.5,0.5,0.5], **kwargs):
        editedRGB = rgb + [1]
        for i in range(2):
            editedRGB[i] -= .2
        self.rgb = editedRGB
        super(cButton, self).__init__(**kwargs)
class xcLabel(Label):
    def __init__(self, rgb=[(14/255),(201/255),(170/255)], **kwargs):
        self.rgb = rgb + [1]
        super(xcLabel, self).__init__(**kwargs)

#ascii table setup:
#                                         #
#-----------------------------------------#
#- - - - - - - - - - - - - - - - - - - - -#

#the following functions are for decluttering the scr functions     #---examples------------------------------#
#large button/label witdh div by 2                                  #-----------------------------------------#
def smallButton(txt, rgb=[.5,.5,.5], height=.1666666666666667):     # the add capacity to low goal buttons    #
    return cButton(text=txt, rgb=rgb, size_hint=(.115, height))     #-----------------------------------------#
def smallLabel(txt, rgb=[.5,.5,.5], height=.1666666666666667):      # fouls/tfouls label and disp             #
    return cLabel(text=txt, rgb=rgb, size_hint=(.115, height))      #-----------------------------------------#
                                                                    #                                         #
                                                                    #large side button/label width div by 2                             #-----------------------------------------#
def smallSideButton(txt, rgb=[.5,.5,.5], height=.1666666666666667): # low goal add and subtract buttons       #
    return cButton(text=txt, rgb=rgb, size_hint=(.0775, height))    #-----------------------------------------#
def smallSideLabel(txt, rgb=[.5,.5,.5], height=.1666666666666667):  # high goal / miss high goal label        #
    return cLabel(text=txt, rgb=rgb, size_hint=(.0775, height))     #-----------------------------------------#
                                                                    #                                         #
#full size buttons and labels for the middle of the UI              #-----------------------------------------#
def largeButton(txt, rgb=[.5,.5,.5], height=.1666666666666667):     # notes button, menu button               #
    return cButton(text=txt, rgb=rgb, size_hint=(.23, height))      #-----------------------------------------#
def largeLabel(txt, rgb=[.5,.5,.5], height=.1666666666666667):      # capacity label                          #
    return cLabel(text=txt, rgb=rgb, size_hint=(.23, height))       #-----------------------------------------#

#full size buttons and labels for the side of the UI                #                                         #
#large button not needed                                            #-----------------------------------------#
def largeSideLabel(txt, rgb=[.5,.5,.5], height=.1666666666666667):  # low goal disp                           #
    return cLabel(text=txt, rgb=rgb, size_hint=(.155, height))      #-----------------------------------------#
def largeSideButton(txt, rgb=[.5,.5,.5], height=.1666666666666667):
    return cButton(text=txt, rgb=rgb, size_hint=(.155, height))
                                                                    #                                         #
#half heightened buttons and labels for prettying                   #-----------------------------------------#
def xlargeSideLabel(txt, rgb=[.5,.5,.5], height=.08333333333):      # high goal / low goal label              #
    return cLabel(text=txt, rgb=rgb, size_hint=(.155, height))      #-----------------------------------------#
def xlargeLabel(txt, rgb=[.5,.5,.5], height=.08333333333):          # round disp                              #
    return cLabel(text=txt, rgb=rgb, size_hint=(.23, height))       #-----------------------------------------#
def xlargeButton(txt, rgb=[.5,.5,.5], height=.08333333333):         # climbed button                          #
    return cButton(text=txt, rgb=rgb, size_hint=(.23, height))      #-----------------------------------------#

#all buttons and labels in the auton screen
def autonLabel(txt, rgb=[.5,.5,.5]):
    return cLabel(text=str(txt), rgb=rgb, size_hint=((1/3), (1/6)))
def autonButton(txt, rgb=[.5,.5,.5]):
    return cButton(text=str(txt), rgb=rgb, size_hint=((1/3), (1/6)))
def smallautonButton(txt, rgb=[.5,.5,.5]):
    return cButton(text=str(txt), rgb=rgb, size_hint=((1/6), (1/6)))
def smallautonLabel(txt, rgb=[.5,.5,.5]):
    return cLabel(text=str(txt), rgb=rgb, size_hint=((1/6), (1/6)))

class Team:
    def __init__(self, number):
        #constants
        self.number = number
        self.highgoal = 0
        self.lowgoal = 0
        self.gears = 0
        self.Foul = 0
        self.TFoul = 0
        #teleop
        self.climb = 0 #whether or not the team climbed
        self.pickupGears = 0
        self.pickupBalls = 0
        self.capacity = 0
        self.AtpGears = 0
        self.MissHighGoal = 0 #attempts
        self.prevnotes = '' #simply notes
        self.posfin = 1 #numerical representation of tog
        self.tog = 'boiler' #where the drive team is in accordance to the boiler
        self.togcolor = [(117/255), (117/255), (117/255)]
        #auton
        self.aHighgoal = 0
        self.aLowgoal = 0
        self.gfin = 0
        self.g = 'never atp the gear'
        self.gfing = 'never atp the gear'
        self.gcolor = [(117/255), (117/255), (117/255)]
        self.aCrossed = 0 #crossed the base line
        self.color = False #True if blue, False if red
        self.wg = 0
        self.w = 'no gear auton'
        self.wgn = 'no gear auton'
        self.wcolor = [0, 0, 0,]

    def getAttr(self): #used in saving and uploading, dumps all vars
        debug("getAttr()", "header 2")
        debug(vars(self))
        return vars(self)
        debug("getAttr() end", "header 2")

    def putData(self, data): #puts the data from the local database into the object
        mapping = {'none':0, 'far':1, 'mid':2, 'boi':3}
        rmapping = {0:'none', 1:'far', 2:'mid', 3:'boi'}
        debug("putData()", "header")
        debug(data)
        data = list(data)
        for i in range(len(data)):
            if data[i] == None: #shouldn't need to be done, but fixing up sqlite3 NULL so that its zero
                debug("Sql nonetype failsafe is being run, this might be a problem")
                data[i] = 0
        debug(str(len(data)))
        try: #getting all of the data out of the fetchone statement earlier
            #next few lines are compressed to save space and for no other reason, it is safe to replace the semicolons with newlines

            self.gears=data[4]; self.highgoal=data[5]; self.lowgoal=data[6]; self.climb=data[14]; self.capacity=data[7]; self.pickupBalls=data[8]
            self.pickupGears=data[9]; self.aLowgoal=data[11]; self.aHighgoal=data[10]; self.gfin=data[12]; self.aCrossed=data[13]; self.color=data[15]
            debug('ooOOOooOOO working')
            self.AtpGears=data[16]; self.MissHighGoal=data[17]; self.prevnotes=data[18]; self.posfin=data[19]; self.Foul=data[20]
            self.TFoul=data[21]; self.wg=mapping[data[22]]
            print(self.wg)
        except:
            debug("whoops, putdata got an error")
            debug("heres data stuff: %s" % data)
        debug("end putData()", "header")

    def putCData(self, c): #puts all the constant data from the local database into the object
        debug("putCData()", "header")
        c.execute("SELECT * FROM `team` WHERE `team`=?", (self.number,))
        data = c.fetchone()
        if data:
            data = list(data)
            for i in range(len(data)):
                if data[i] == None:
                    data[i] = 0
        else:
            debug("data is lame-o, doesn")
        try:
            self.capacity=data[1]; self.pickupBalls=data[2]; self.pickupGears=data[3]; debug(data[1])
        except:
            debug('ok')
        debug("putCData() end", "header")

class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.25
            if vel.length() >= 80:
                vel = bounced * 1
            ball.velocity = vel.x, vel.y + offset
            print (vel.length())

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    parentscreen = None

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))
        if self.player1.score == 4:
            self.parentscreen.win = "P1 Wins"
            self.player1.score = 0
            self.parentscreen.scrMain()
        if self.player2.score == 4:
            self.parentscreen.win = "P2 Wins"
            self.player2.score = 0
            self.parentscreen.scrMain()

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

game = PongGame()

#main class, overwrites stacklayout layout from kivy
class Screen(StackLayout):
    timeDisp = None
    prev = ''
    mapping = {'none':0, 'far':1, 'mid':2, 'boi':3}
    rmapping = {0:'none', 1:'far', 2:'mid', 3:'boi', }

    #save above

    def __init__(self, **kwargs):

        super(Screen, self).__init__(**kwargs)
        self.lastLowVal = 0
        self.choose()

        self.konami = []
        self.canPong = True

    def makeDB(self, db): #makes the database framework if it doesn't exist
        debug("makeDB()", "header")
        db.execute('''CREATE TABLE IF NOT EXISTS `main`(
                      `round` INTEGER NOT NULL,
                      `team` INTEGER NOT NULL,
                      `scouterName` TEXT NOT NULL,
                      `event` INTEGER,
                      `gears` INTEGER,
                      `highgoal` INTEGER,
                      `lowgoal` INTEGER,
                      `capacity` INTEGER,
                      `pickupBalls` INTEGER,
                      `pickupGears` INTEGER,
                      `aHighgoal` INTEGER,
                      `aLowgoal` INTEGER,
                      `aGears` INTEGER,
                      `aCrossed` INTEGER,
                      `climbed` INTEGER,
                      `team color` INTEGER,
                      `AtpGears` INTEGER,
                      `MissHighGoal` INTEGER,
                      `notes` TEXT,
                      `position` INTEGER,
                      `Foul` INTEGER,
                      `TFoul` INTEGER,
                      `AGear Pos` TEXT
                      )''')
        db.execute("CREATE TABLE IF NOT EXISTS `lastscouter` (`name` TEXT, `color` INTEGER)")
        db.execute('''CREATE TABLE IF NOT EXISTS `team`(
                      `team`INTEGER NOT NULL,
                      `capacity` INTEGER,
                      `pickupBalls` INTEGER,
                      `pickupGears` INTEGER,
                      PRIMARY KEY(`team`))''')
        db.execute("CREATE TABLE IF NOT EXISTS `events` (`currentEvent` TEXT)")
        debug("makeDB() end", "header")

    def getlastscouter(self, default='', wh='name'): #returns last scouter it remembers
        debug("getLastScouter()", "header")
        #opening up the database
        db = sqlite3.connect('rounddat.db')
        self.makeDB(db)
        pos = db.cursor()
        res = pos.execute('SELECT * FROM lastscouter')
        row = pos.fetchone()
        #finishing work in database
        pos.close()
        db.close()
        if row == None:
            return default
        else:
            if wh =='name':
                return row[0]
            else:
                return row[1]
        debug("getLastScouter() end", "header")

    def setlastscouter(self, name, color): #puts last scouter into memory
        debug("setlastscouter()", "header")
        debug(name)
        if self.getlastscouter(None) == None:
            scouterexist = False
        else:
            scouterexist = True
        db = sqlite3.connect ('rounddat.db')
        if scouterexist:
            db.execute("UPDATE `lastscouter` SET `name`=?, `color`=?", (name, color))
        else:
            db.execute("INSERT INTO `lastscouter`(`name`, `color`) VALUES (?, ?);", (name, color))
        db.commit()
        db.close()
        debug("setlastscouter() end", "header")

    def choose(self, hint="", obj=None): #scr to choose team, round and scouter
        debug("choose()", "title")
        self.clear_widgets()
        displist = list()
        #                      setting up color                    setting up text            setting up size
        displist.append(cLabel(rgb=[(14/255),(201/255),(170/255)], text="Enter team number:", size_hint=(.5, .25)))
        self.teamsel =  TextInput(hint_text=hint,multiline=False,size_hint=(.5, .25)) #this text box needs to be associated with the class to get the text within it later
        displist.append(self.teamsel)
        #same as above
        displist.append(cLabel(rgb=[(14/255),(201/255),(170/255)], text="Enter round number:", size_hint=(.5, .25)))
        self.roundsel = TextInput(hint_text=hint, multiline=False, size_hint=(.5, .25)) #same as above
        displist.append(self.roundsel)
        #same as above, will be bound to go to teleop screen
        displist.append(cLabel(rgb=[(14/255),(201/255),(170/255)], text="Enter your full name:", size_hint=(.5, .25)))
        self.name = TextInput(multiline=False, size_hint=(.5, .25), text=self.getlastscouter(wh="name")) #pulls from database
        displist.append(self.name)
        #button to click to get into the main screen
        gobutton = cButton(text="Go", size_hint=(1, .25), padding=[10,10]); displist.append(gobutton) #not being appended directly because we need to bind it to pressGo method
        self.name.bind(on_text_validate=self.pressGo)
        gobutton.bind(on_release=self.pressGo)

        for widg in displist:
            self.add_widget(widg)
        debug("choose() end", "title")

    def failSetTeam(self):
        debug("failSetTeam()", "header 2")
        debug("unable to setTeam, number %s, round %s" % (self.teamsel.text, self.roundsel.text))
        debug("failSetTeam() end", "header 2")
        self.choose(hint="Enter a number value.")

    def pressGo(self, obj): #called to set things up before heading to main scr
        debug("pressGo()", "title")
        numbers = "1234567890"
        debug(numbers)
        debug(self.teamsel.text)
        debug(self.roundsel.text)
        if not self.teamsel.text or not self.roundsel.text:
            self.failSetTeam()
            return
        for i in self.teamsel.text:
            if not i in numbers:
                self.failSetTeam()
                return
        for i in self.roundsel.text:
            if not i in numbers:
                self.failSetTeam()
                return
        self.setTeam(self.teamsel.text, self.roundsel.text, self.name.text)
        self.setlastscouter(self.name.text, self.team.color )
        debug("pressGo() end", "title")

    def setTeam(self, team, round, name): #gets the team name from the shared database in the raspberry pi
        debug("setTeam()", "title")
        #unpack info sent by pressGo method
        if not team == "came from handleEvent":
            self.team = Team(team)
            self.team.round = round #it renamed a method but it still works don't question it
            self.team.scouterName = name

        dbl = sqlite3.connect("rounddat.db") #connect to local database
        cl = dbl.cursor()
        self.makeDB(cl)

        self.team.prevnotes = "" #reinitialize notes??? may need to be removed

        cl.execute("SELECT * FROM `team` WHERE `team`=?", (self.team.number,))
        found = cl.fetchone() #returns None if there is no data
        if not found:
            dbl.execute("INSERT INTO `team`(`team`) VALUES (?);", (self.team.number,))
            dbl.commit()
        else:
            self.team.putCData(cl)

        try: #remake the database if not found
            cl.execute("SELECT * FROM `main` WHERE `round`=? AND `team`=? AND `event`=?", (self.team.round, self.team.number, CURRENT_EVENT)) #this will error if the main table isnt there
            found = cl.fetchone()
        except:
            debug("had to remake db")
            self.makeDB(cl)
            found = False
        if not found:
            debug("putting data into main...")
            dbl.execute("INSERT INTO `main`(`round`,`team`,`scouterName`,`event`) VALUES (?,?,?,?);", (self.team.round, self.team.number, self.team.scouterName, CURRENT_EVENT))
            debug("round: %s, team: %s, scouter: %s, event: %s", (round, team, name, CURRENT_EVENT))
            dbl.execute("UPDATE `main` SET `scouterName`=? WHERE `round`=? AND `team`=? AND `event`=?", (self.team.scouterName, self.team.round, self.team.number, CURRENT_EVENT))
            dbl.commit()
        else:
            self.team.putData(found)
        debug(self.team.color)

        #grabbing team's color and making the color correct
        if self.team.color == None: #default
            self.team.color = self.getlastscouter(default=True, wh='color')
        elif self.team.color == 1: #sqlite can't handle bools
            self.team.color == True
        else:
            self.team.color = False

        if self.team.color == False:
            debug('color is false (red)')
            self.buttoncolor = [(200/255), 0, 0]
        else:
            debug("color is true (blue)")
            self.buttoncolor =[0, 0,(200/255)]
        #grabbing team's position and correcting color
        if self.team.posfin == 1:
            self.team.tog = '2'
            self.team.togcolor = [(117/255), (117/255), (117/255)]
        elif self.team.posfin == 2:
            self.team.tog = '3'
            self.team.togcolor = [0, (255/255), (42/255)]
        else:
            self.team.tog = '1'
            self.team.togcolor = [(235/255), (61/255), (255/255)]
        debug("pos color", "header 2")
        debug(self.team.posfin)

        if self.team.gfin == 0:
            self.team.g = 'never attempted the gear'
            self.team.gcolor = [(117/255), (117/255), (117/255)]
            self.team.gfing = 'made the gear'
        elif self.team.gfin == 1:
            self.team.g = 'made the gear'
            self.team.gcolor = [0, (255/255), (42/255)]
            self.team.gfing = 'never attempted the gear'
        self.setAGP()

        debug(self.team.color)
        cl.close()
        dbl.close()
        debug("setTeam() end", "title")
        self.scrAuton()

        eventname = CURRENT_EVENT
        db = sqlite3.connect('rounddat.db')
        db.execute("INSERT INTO `events`(`currentEvent`) VALUES (?)", (eventname,))
        db.commit()
        db.close()
        #self.setTeam("came from handleEvent", None, None)
        return

    #the following functions are called by the buttons on the interface when pressed
    def addLow(self, count, widg): #add to low goals scored
        debug("addLow()")
        self.reloadList = [widg]
        self.team.lowgoal += count
        if self.team.lowgoal <= 0:
            self.team.lowgoal = 0
        widg.text = str(self.team.lowgoal)
        if count > 0: self.konami.append("up")
        if count < 0: self.konami.append("down")
        debug(self.konami[-10:])
        if self.konami[-10:] == ["a", "b", "right", "left", "right", "left", "down", "down", "up", "up"]:
            self.canPong = not self.canPong
            debug("can pong: " + str(self.canPong))
    def addHigh(self, count, widg): #add to high goals scored
        debug("addHigh()")
        self.reloadList = [widg]
        self.team.highgoal += count
        if self.team.highgoal <= 0:
            self.team.highgoal = 0
        widg.text = str(self.team.highgoal)
        if count > 0: self.konami.append("left")
    def addMissHigh(self, count, widg): #add to missed high goals
        debug("addMissHigh()")
        self.reloadList = [widg]
        self.team.MissHighGoal += count
        if self.team.MissHighGoal <= 0:
            self.team.MissHighGoal = 0
        widg.text = str(self.team.MissHighGoal)
        if count > 0: self.konami.append("right")
    def addGear(self, count, widg, atpwidg): #add to gears scored
        debug("addGear()")
        self.reloadList = [widg]
        self.team.gears += count
        if self.team.gears <= 0:
            self.team.gears = 0
        if self.team.gears > self.team.AtpGears:
            self.team.AtpGears = self.team.gears
            self.addatpGear(0, atpwidg)

        widg.text = str(self.team.gears)
        if count > 0: self.konami.append("a")
        if count < 0: self.konami.append("b")
        debug(self.konami[-10:])
        try:
            if self.konami[-10:] == ["up", "up", "down", "down", "left", "right", "left", "right", "b", "a"] and self.canPong:
                game.serve_ball()
                game.parentscreen = self
                Clock.schedule_interval(game.update, 1.0 / 60.0)
                self.clear_widgets()
                self.add_widget(game)
        except IndexError:
            self.konami = []
    def Foul(self, count, widg): #add to the foul count
        debug("Foul()")
        self.reloadList = [widg]
        self.team.Foul += count
        if self.team.Foul <= 0:
            self.team.Foul = 0
        widg.text = str(self.team.Foul)
    def TFoul(self, count, widg): #add to the tech foul count
        debug("TFoul()")
        self.reloadList = [widg]
        self.team.TFoul += count
        if self.team.TFoul <= 0:
            self.team.TFoul = 0
        widg.text = str(self.team.TFoul)
    def addatpGear(self, count, widg): #add to attempted gears
        debug("addatpGear")
        self.reloadList = [widg]
        self.team.AtpGears += count
        if self.team.AtpGears <= 0:
            self.team.AtpGears = 0
        widg.text = str(self.team.AtpGears)
    def canPickGear(self, widg, obj=None): #toggle the ability to pick up gears
        debug("canPickGear()")
        self.reloadList = [widg]
        self.team.pickupGears = int(not self.team.pickupGears)
        widg.text = "The robot %s pickup gears off of the ground." % ("CAN" if self.team.pickupGears else "CAN'T")
    def canPickBall(self, widg, obj=None): #toggle the ability to pick balls off ground
        debug("canPickBall")
        self.reloadList = [widg]
        self.team.pickupBalls = int(not self.team.pickupBalls)
        widg.text = "The robot %s pickup balls off of the ground." % ("CAN" if self.team.pickupBalls else "CAN'T")
    def climbed(self, widg, mode="Start", obj=None): #toggle whether or not the team climbed
        debug("climbed()")
        if mode == "Start":
            self.climbStart = time.time()
            Clock.schedule_interval( self.updateClock, .01 )
        if mode == "Stop":
            Clock.unschedule( self.updateClock )
            climbEnd = time.time()
            climbDiff = str( round( (climbEnd - self.climbStart), 2) )[:3]
            debug(climbDiff)
            self.team.climb = float(climbDiff)
            widg.text = str(climbDiff)
        if mode == "None":
            Clock.unschedule( self.updateClock )
            self.team.climb = 0
            widg.text = "0"
    def color(self, widg, obj=None): #toggle the team color (red, blue)
        debug("color")
        self.reloadList = [widg]
        self.team.color = int(not self.team.color)
        debug('color run')
        if self.team.color:
            self.buttoncolor = [0, 0, (200/255)]
        else:
            self.buttoncolor =[(200/255), 0, 0]
        self.scrMain()
    def aAddLow(self, count, widg): #add to auton low goal count
        debug("aAddLow")
        self.reloadList = [widg]
        self.team.aLowgoal += count
        if self.team.aLowgoal <= 0:
            self.team.aLowgoal = 0
        widg.text = str(self.team.aLowgoal)
    def aAddHigh(self, count, widg): #add to auton high coal count
        debug("aAddHigh()")
        self.reloadList = [widg]
        self.team.aHighgoal += count
        if self.team.aHighgoal <= 0:
            self.team.aHighgoal = 0
        widg.text = str(self.team.aHighgoal)
    def checkg(self, widg, obj=None): #toggle if team used gear in auton
        self.reloadList = [widg]
        self.team.gfin = self.team.gfin + 1
        debug(self.team.gfing)
        if self.team.gfin >= 2:
            self.team.gfin = self.team.gfin - 2
        if self.team.gfin == 1:
            self.team.g = 'made the gear'
            self.team.gcolor = [0, (255/255), (42/255)]
            self.team.gfing = 'never atp the gear'
        else:
            self.team.g = 'never atp the gear'
            self.team.gcolor = [(117/255), (117/255), (117/255)]
            self.team.gfing ='made the gear'
        widg.text=self.team.g
        widg.background_color=self.team.gcolor + [1]

    def linkCrossAGear(self, widg, basslinewidg):
        print('1235412734213642816342561')
        self.checkg(widg)
        if self.team.gfin == 1:
            print('111111111111111111111111111111111')
            if self.team.aCrossed == 0:
                print('yyyyyyyyyyyyyyyyyyy')
                self.aToggleCross(basslinewidg)
    def aToggleCross(self, widg, obj=None): #toggle if team crossed base line in auton
        debug("aToggleCross")
        self.reloadList = [widg]
        self.team.aCrossed = int(not self.team.aCrossed)
        widg.text = "The team %s cross the ready line."%("DID"if self.team.aCrossed else"DIDN'T")
    def checkwg(self, widg, obj=None): #toggle if team used gear in auton
        self.reloadList = [widg]
        self.team.wg = self.team.wg + 1
        debug(self.team.wgn)
        self.mapping = {0:'None', 1:'far', 2:'mid', 3:'boiler'}
        if self.team.wg >= 4:
            self.team.wg = self.team.wg - 4
        self.setAGP()

        self.scrAuton()
    def setAGP(self):
        if self.team.wg == 1:
            self.team.w = 'far'
            self.team.wcolor = [(117/255), (117/255), (117/255)]
            self.team.wgn = 'mid'
        elif self.team.wg == 2:
            self.team.w = 'mid'
            self.team.wcolor = [0, (255/255), (42/255)]
            self.team.wgn = 'boiler'
        elif self.team.wg == 3:
            self.team.w = 'boiler'
            self.team.wcolor = [(235/255), (61/255), (255/255)]
            self.team.wgn = 'no gear auton'
        else:
            self.team.w = 'no gear auton'
            self.team.wcolor = [0, 0, 0,]
            self.team.wgn ='far'
        print(self.team.wg)
    def updateClock(self, widg, obj=None):
        self.timeDisp.text = str( round( (time.time() - self.climbStart), 2) )[:3]

    #main functions (displays)
    def scrMain(self, obj=None):
        debug("scrMain()", "title")
        Clock.unschedule(game.update)
        displist = list()
        self.camefrom = "tele" #used to route the cancel button on the areyousure scr
        #reset menu button text
        self.didSave = "save"
        self.didUpload = "               Upload \n (Save before uploading)"
        self.didUploadAll = "            Upload all \n (Save before uploading)"

            #line 1
        climbLbl =     xlargeSideLabel("Climb", rgb=[(14/255),(201/255),(170/255)]); displist.append(climbLbl)
        spaceLbl =     xlargeLabel("", rgb=[0, 0, 0, 1]); displist.append(spaceLbl)
        teamDisp =     xlargeButton(txt="Team " + str(self.team.number), rgb=[0, 0, 0]); teamDisp.bind(on_release=self.scrTeam); displist.append(teamDisp)
        scouterDisp =  xlargeLabel("Scouter " + str(self.team.scouterName), rgb=[0, 0, 0, 1]); displist.append(scouterDisp)
        highLbl =      xlargeSideLabel("kPa", rgb=[(28/255),(201/255),(40/255)]); displist.append(highLbl) #cheesing so that we don't have to make two labels

            #line 2
        spaceLbl1=     xlargeSideLabel("", rgb=[(14/255),(201/255),(170/255)]); displist.append(spaceLbl1)
        spaceLbl2 =    xcLabel(text="", rgb=[0, 0, 0], size_hint=(.23, .075)); displist.append(spaceLbl2)
        roundBtn =     xlargeButton(txt="Round " + str(self.team.round), rgb=[0, 0, 0]); roundBtn.bind(on_release=self.scrRound); displist.append(roundBtn)
        eventDisp =    xlargeLabel("Event " + str(CURRENT_EVENT), rgb=[0, 0, 0, 1]); displist.append(eventDisp)
        spaceLbl3 =    xlargeSideLabel("", rgb=[(28/255),(201/255),(40/255)]); displist.append(spaceLbl3) #cheesing so that we don't have to make two labels

            #line 3
        self.timeDisp =largeSideLabel(str(self.team.climb), rgb=[(14/255),(201/255),(170/255)]); displist.append(self.timeDisp)
        checkColor =   largeButton("Team Blue" if self.team.color else "Team Red", rgb=self.buttoncolor); checkColor.bind(on_release=lambda x: self.color(checkColor)); displist.append(checkColor)
        #checkClimb1 =  smallButton("climbed" if self.team.climb else "didn't climb", rgb=[(201/255),(28/255),(147/255)]); checkClimb1.bind(on_release=lambda x: self.climbed(checkClimb1)); displist.append(checkClimb1)
        teleopLbl =    largeLabel("Teleop", rgb=[0, 0, 0, 1]); displist.append(teleopLbl)
        toggleExit =   largeButton("Menu", rgb=[(201/255),(170/255),(28/255)]); toggleExit.bind(on_release=self.scrExit); displist.append(toggleExit)
        highDisp =     largeSideLabel(str(self.team.highgoal), rgb=[(28/255),(201/255),(40/255)]); displist.append(highDisp)

            #line 4
        climbStartBtn =largeSideButton("Started climbing", rgb=[(14/255),(201/255),(170/255)]); climbStartBtn.bind(on_release=lambda x: self.climbed(self.timeDisp, mode="Start")); displist.append(climbStartBtn)
        #decLow3 =      smallSideButton("-3", rgb=[(14/255),(201/255),(170/255)]); decLow3.bind(on_release=lambda x: self.addLow(-3, lowDisp)); displist.append(decLow3)
        FoulLbl =      smallLabel("Fouls", rgb=[(28/255),(129/255),(201/255)]); displist.append(FoulLbl)
        FoulDisp =     smallLabel(str(self.team.Foul), rgb=[(28/255),(129/255),(201/255)]); displist.append(FoulDisp)
        TFoulLbl =     smallLabel("TFouls", rgb=[(28/255),0,(201/255)]); displist.append(TFoulLbl)#AtpGears is the varible for Miss Gears
        TFoulDisp =    smallLabel(str(self.team.TFoul), rgb=[(28/255),0,(201/255)]); displist.append(TFoulDisp)
        toggleAuton =  smallButton("Auton", rgb=[(201/255),(170/255),(28/255)]); toggleAuton.bind(on_release=self.scrAuton); displist.append(toggleAuton)
        toggleCapab =  smallButton("Capability", rgb=[(201/255),(170/255),(28/255)]); toggleCapab.bind(on_release=self.scrCapab); displist.append(toggleCapab)
        decHigh =      largeSideButton("-1", rgb=[(28/255),(201/255),(40/255)]); decHigh.bind(on_release=lambda x: self.addHigh(-1, highDisp)); displist.append(decHigh)

            #line 5
        climbStopBtn =largeSideButton("Finished climbing", rgb=[(14/255),(201/255),(170/255)]); climbStopBtn.bind(on_release=lambda x: self.climbed(self.timeDisp, mode="Stop")); displist.append(climbStopBtn)
        #decLow15 =    smallSideButton("-15", rgb=[(14/255),(201/255),(170/255)]); decLow15.bind(on_release=lambda x: self.addLow(-15, lowDisp)); displist.append(decLow15)
        addFoul =     smallButton("+", rgb=[(28/255),(129/255),(201/255)]); addFoul.bind(on_release=lambda x: self.Foul(1, FoulDisp)); displist.append(addFoul)
        decFoul =     smallButton("-", rgb=[(28/255),(129/255),(201/255)]); decFoul.bind(on_release=lambda x: self.Foul(-1, FoulDisp)); displist.append(decFoul)
        addTFoul =    smallButton("+", rgb=[(28/255),0,(201/255)]); addTFoul.bind(on_release=lambda x: self.TFoul(1, TFoulDisp)); displist.append(addTFoul)
        decTFoul =    smallButton("-", rgb=[(28/255),0,(201/255)]); decTFoul.bind(on_release=lambda x: self.TFoul(-1, TFoulDisp)); displist.append(decTFoul)
        togglenotes = largeButton("Notes", rgb=[(201/255),(170/255),(28/255)]); togglenotes.bind(on_release=self.scrnotes); displist.append(togglenotes)
        addHigh1 =    largeSideButton("-3", rgb=[(28/255),(201/255),(40/255)]); addHigh1.bind(on_release=lambda x: self.addHigh(-3, highDisp)); displist.append(addHigh1)

            #line 6
        noClimbBtn =  largeSideButton("Reset", rgb=[(14/255),(201/255),(170/255)]); noClimbBtn.bind(on_release=lambda x: self.climbed(self.timeDisp, mode="None")); displist.append(noClimbBtn)
        #incLow3 =     smallSideButton("3", rgb=[(14/255),(201/255),(170/255)]); incLow3.bind(on_release=lambda x: self.addLow(3, lowDisp)); displist.append(incLow3)
        capLbl =      largeLabel("Capacity", rgb=[(14/255),(201/255),(170/255)]); displist.append(capLbl)
        gearLbl =     smallLabel("Gears", rgb=[(28/255),(129/255),(201/255)]); displist.append(gearLbl)
        gearDisp =    smallLabel(str(self.team.gears), rgb=[(28/255),(129/255),(201/255)]); displist.append(gearDisp)
        atpGearLbl =  smallLabel("AtpGears", rgb=[(28/255),0,(201/255)]); displist.append(atpGearLbl)#AtpGears is the varible for Miss Gears
        atpGearDisp = smallLabel(str(self.team.AtpGears), rgb=[(28/255),0,(201/255)]); displist.append(atpGearDisp)
        addHigh2 =    largeSideButton("+1", rgb=[(28/255),(201/255),(40/255)]); addHigh2.bind(on_release=lambda x: self.addHigh(1, highDisp)); displist.append(addHigh2)

            #line 7
        spaceLbl4 =   largeSideLabel("Note: if a robot\nfails to climb,\nreset the timer\nto 0.", rgb=[(14/255),(201/255),(170/255)]); displist.append(spaceLbl4)
        capDispAdd =   smallButton("+" + str(self.team.capacity), rgb=[(14/255),(201/255),(170/255)]); capDispAdd.bind(on_release=lambda x: self.addLow(self.team.capacity, lowDisp)); displist.append(capDispAdd)
        capDispSub =   smallButton("-" + str(self.team.capacity), rgb=[(14/255),(201/255),(170/255)]); capDispSub.bind(on_release=lambda x: self.addLow(-self.team.capacity, lowDisp)); displist.append(capDispSub)
        addGear =      smallButton("+", rgb=[(28/255),(129/255),(201/255)]); displist.append(addGear)
        decGear =      smallButton("-", rgb=[(28/255),(129/255),(201/255)]); displist.append(decGear)
        addatpGear =   smallButton("+", rgb=[(28/255),0,(201/255)]); addatpGear.bind(on_release=lambda x: self.addatpGear(1, atpGearDisp)); displist.append(addatpGear)
        decatpGear =   smallButton("-", rgb=[(28/255),0,(201/255)]); decatpGear.bind(on_release=lambda x: self.addatpGear(-1, atpGearDisp)); displist.append(decatpGear)
        decGear.bind(on_release=lambda x: self.addGear(-1, gearDisp, atpGearDisp))
        addGear.bind(on_release=lambda x: self.addGear(1, gearDisp, atpGearDisp))
        addHigh3 =     largeSideButton("+3", rgb=[(28/255),(201/255),(40/255)]); addHigh3.bind(on_release=lambda x: self.addHigh(3, highDisp)); displist.append(addHigh3)

        self.clear_widgets()
        for widg in displist:
            self.add_widget(widg)
        debug("scrMain() end", "title")

    def scrExit(self, obj=None): #menu scr
        debug("scrExit()", "title")
        displist = list()
        self.camefrom = "exit"
        #row 1
        cancel =   Button(text="Cancel", size_hint=(1,.1)); cancel.bind(on_release=self.scrMain); displist.append(cancel)
        #row 2
        saveExit = Button(text=self.didSave, size_hint=(.25,.8)); saveExit.bind(on_release=self.save); displist.append(saveExit)
        upload = Button(text=self.didUpload, size_hint=(.25,.8)); upload.bind(on_release=self.upload); displist.append(upload)
        uploadAll = Button(text=self.didUploadAll, size_hint=(.25,.8)); uploadAll.bind(on_release=self.uploadAll); displist.append(uploadAll)
        Team = Button(text="Team", size_hint=(.25,.8)); Team.bind(on_release=lambda x: self.areYouSure("tele")); displist.append(Team)
        #row 3
        exit =     Button(text="Exit", size_hint=(1, .1)); exit.bind(on_release=lambda x: self.areYouSure("exit")); displist.append(exit)

        self.clear_widgets()
        for widg in displist:
            self.add_widget(widg)
        debug("scrExit() end", "title")

    def scrCapab(self, obj=None, cap=None, reload=False): #cabapilities scr
        debug("scrCapab()", "title")
        displist = list()
        capChangeText = ""
        if not cap == None:
            try:
                self.team.capacity = int(cap)
            except:
                capChangeText = "Enter a number value."

        #presetting messages on buttons so that it doesn't clutter
        PBMessage = "The robot %s pickup balls off of the ground." % ("CAN" if self.team.pickupBalls else "CAN'T")
        PGMessage = "The robot %s pickup gears off of the ground." % ("CAN" if self.team.pickupGears else "CAN'T")

        #row 1
        cancel = cButton(text="Cancel", size_hint=(1, .1)); cancel.bind(on_release=self.scrMain if self.camefrom == "tele" else self.scrAuton); displist.append(cancel)
        #row 2
        togglePG = cButton(text=PGMessage, rgb=[(201/255),(28/255),(147/255)], size_hint=(.5, .45)); togglePG.bind(on_release=self.canPickGear); displist.append(togglePG)
        togglePB = cButton(text=PBMessage, rgb=[(201/255),(28/255),(147/255)], size_hint=(.5, .45)); togglePB.bind(on_release=self.canPickBall); displist.append(togglePB)
        #row 3
        capLbl = cLabel(text="Capacity:\n%s" % self.team.capacity, rgb=[(201/255),(28/255),(147/255)], size_hint=(.5, .45)); displist.append(capLbl)
        capChange = TextInput(hint_text=capChangeText, multiline=False, size_hint=(.5, .45)); capChange.bind(on_text_validate=lambda x: self.scrCapab(cap=capChange.text)); displist.append(capChange)

        self.clear_widgets()
        for widg in displist:
            self.add_widget(widg)
        debug("scrCapab() end", "title")

    def savednotes(self, notesfield): #saving notes
        debug("savednotes()", "title")
        self.team.prevnotes = notesfield.text
        debug(self.team.prevnotes)
        debug(notesfield.text)
        debug("savednotes() end", "title")
        self.scrMain()

    def scrnotes(self, obj=None, cap=None): #notes scr
        debug("scrnotes()", "title")
        self.clear_widgets()
        displist = list()
        notesText = str(self.team.prevnotes) #puts original notes back in

        #row 1
        save = cButton(text="Save", size_hint=(1, .1)); save.bind(on_release=lambda x: self.savednotes(notes)); displist.append(save)
        #row 2
        notes = TextInput(text=str(self.team.prevnotes), multiline=True, size_hint=(1, .8)); notes.bind(on_text_validate=lambda x: self.scrnotes); displist.append(notes)
        #row 3
        cancel = cButton(text="Cancel", size_hint=(1, .1)); cancel.bind(on_release=self.scrMain if self.camefrom == "tele" else self.scrAuton); displist.append(cancel)

        for widg in displist:
            self.add_widget(widg)
        debug("scrnotes() end", "title")

    def scrAuton(self, obj=None, reload=False): #autonomous scr
        debug("scrAuton()", "title")
        displist = list()
        self.reloadlist = list()
        self.camefrom = "auton"


        #row 1
        lowLbl =  autonLabel(txt="Low", rgb=[(14/255),(201/255),(170/255)]); displist.append(lowLbl)
        teamLbl = smallautonLabel(txt="Team " + str(self.team.number), rgb=[0, 0, 0, 1]); displist.append(teamLbl)
        roundLbl = smallautonLabel(txt='Round ' + str(self.team.round), rgb=[0, 0, 0, 1]); displist.append(roundLbl)
        highLbl = autonLabel(txt="High", rgb=[(28/255),(201/255),(40/255)]); displist.append(highLbl)
        #row 2
        lowDisp =  autonLabel(txt=self.team.aLowgoal, rgb=[(14/255),(201/255),(170/255)]); displist.append(lowDisp)
        autonLbl = autonLabel(txt="Auton", rgb=[0, 0, 0, 1]); displist.append(autonLbl)
        highDisp = autonLabel(txt=self.team.aHighgoal, rgb=[(28/255),(201/255),(40/255)]); displist.append(highDisp)
        #row 3
        low1 =       autonButton(txt="+1", rgb=[(14/255),(201/255),(170/255)]); low1.bind(on_release=lambda x: self.aAddLow(1, lowDisp)); displist.append(low1)
        toggleTele = smallautonButton(txt="Teleop", rgb=[(201/255),(170/255),(28/255)]); toggleTele.bind(on_release=self.scrMain); displist.append(toggleTele)
        toggleCapab = smallautonButton(txt="Capability", rgb=[(201/255),(170/255),(28/255)]); toggleCapab.bind(on_release=self.scrCapab); displist.append(toggleCapab)
        high1 =      autonButton(txt="+1", rgb=[(28/255),(201/255),(40/255)]); high1.bind(on_release=lambda x: self.aAddHigh(1, highDisp)); displist.append(high1)
        #row 4
        low5 =        autonButton(txt="+5", rgb=[(14/255),(201/255),(170/255)]); low5.bind(on_release=lambda x: self.aAddLow(5, lowDisp)); displist.append(low5)
        #self.timeLbl = autonButton(txt="", rgb=[0, 0, 0]);displist.append(self.timeLbl)
        checkwg =  autonButton(self.team.w, self.team.wcolor); checkwg.bind(on_release=lambda x: self.checkwg(checkwg)); displist.append(checkwg)
        high3 =       autonButton(txt="+3", rgb=[(28/255),(201/255),(40/255)]); high3.bind(on_release=lambda x: self.aAddHigh(3, highDisp)); displist.append(high3)
        #row 5
        lowm1 =   autonButton(txt="-1", rgb=[(14/255),(201/255),(170/255)]); lowm1.bind(on_release=lambda x: self.aAddLow(-1, lowDisp)); displist.append(lowm1)
        checkg =  autonButton(self.team.g, self.team.gcolor); displist.append(checkg)
        highm1 =  autonButton(txt="-1", rgb=[(28/255),(201/255),(40/255)]); highm1.bind(on_release=lambda x: self.aAddHigh(-1, highDisp)); displist.append(highm1)
        #row 6
        lowm5 =  autonButton(txt="-5", rgb=[(14/255),(201/255),(170/255)]); lowm5.bind(on_release=lambda x: self.aAddLow(-5, lowDisp)); displist.append(lowm5)
        xedBtn = autonButton(txt="The team %s cross the ready line."%("DID"if self.team.aCrossed else"DIDN'T"),rgb=[(28/255),(129/255),(201/255)]);xedBtn.bind(on_release=self.aToggleCross);displist.append(xedBtn)
        highm3 = autonButton(txt="-3", rgb=[(28/255),(201/255),(40/255)]); highm3.bind(on_release=lambda x: self.aAddHigh(-3, highDisp)); displist.append(highm3)
        checkg.bind(on_release=lambda x: self.linkCrossAGear(checkg, xedBtn))
        self.clear_widgets()
        for widg in displist:
            self.add_widget(widg)
        debug("scrAuton() end", "title")

    def scrEvent(self, obj=None):
        debug("scrEvent", "title")
        self.clear_widgets()
        displist = list()

        eventLbl = cLabel(text="Event name", size_hint=(.5, .5)); displist.append(eventLbl)
        self.eventTxt = TextInput(multiline=False, size_hint=(.5, .5)); self.eventTxt.bind(on_text_validate=self.handleEvent); displist.append(self.eventTxt)
        goBtn = cButton(text="Go", size_hint=(1, .5)); goBtn.bind(on_release=self.handleEvent); displist.append(goBtn)

        for widg in displist:
            self.add_widget(widg)
        debug("scrEvent end", "title")

    def scrRound(self, obj=None, text=""):
        debug("scrEvent", "title")
        self.clear_widgets()
        displist = list()

        roundLbl = cLabel(text="Round number", size_hint=(.5, .5)); displist.append(roundLbl)
        self.roundTxt = TextInput(hint_text=text, multiline=False, size_hint=(.5, .5)); self.roundTxt.bind(on_text_validate=self.handleRound); displist.append(self.roundTxt)
        goBtn = cButton(text="Go", size_hint=(1, .5)); goBtn.bind(on_release=self.handleRound); displist.append(goBtn)

        for widg in displist:
            self.add_widget(widg)
        debug("scrEvent end", "title")

    def handleRound(self, obj=None):
        if not self.roundTxt.text: return
        for i in self.roundTxt.text:
            if not i in string.digits:
                self.scrRound(text="Enter a number value.")
                return
        dbl = sqlite3.connect("rounddat.db")
        dbl.execute("UPDATE main SET round=? WHERE team=? AND round=? AND event=?", (self.roundTxt.text, self.team.number, self.team.round, CURRENT_EVENT))
        debug(self.roundTxt.text)
        self.team.round = self.roundTxt.text
        dbl.commit()
        dbl.close()
        self.scrMain()

    def scrTeam(self, obj=None, text=""):
        debug("scrEvent", "title")
        self.clear_widgets()
        displist = list()

        teamLbl = cLabel(text="team number", size_hint=(.5, .5)); displist.append(teamLbl)
        self.teamTxt = TextInput(hint_text=text, multiline=False, size_hint=(.5, .5)); self.teamTxt.bind(on_text_validate=self.handleTeam); displist.append(self.teamTxt)
        goBtn = cButton(text="Go", size_hint=(1, .5)); goBtn.bind(on_release=self.handleTeam); displist.append(goBtn)

        for widg in displist:
            self.add_widget(widg)
        debug("scrEvent end", "title")

    def handleTeam(self, obj=None):
        if not self.teamTxt.text: return
        for i in self.teamTxt.text:
            if not i in string.digits:
                self.scrTeam(text="Enter a number value.")
                return
        dbl = sqlite3.connect("rounddat.db")
        dbl.execute("UPDATE main SET team=? WHERE team=? AND team=? AND event=?", (self.teamTxt.text, self.team.number, self.team.round, CURRENT_EVENT))
        debug(self.teamTxt.text)
        self.team.number = self.teamTxt.text
        dbl.commit()
        dbl.close()
        self.scrMain()

    def areYouSure(self, camefrom=None, obj=None): #prompt for leaving saved data
        debug("areYouSure()", "title")
        self.clear_widgets()
        displist = list()
        if not camefrom == None:
            self.camefrom = camefrom

        if self.camefrom == "exit":
            def func(obj=None):
                exit()
        elif self.camefrom == "tele":
            def func(obj=None):
                self.save()
                self.choose()
        else:
            def func(obj=None):
                self.save()
                self.choose()

        AYSLbl = Label(text="Are you sure?", size_hint=(1,.1)); displist.append(AYSLbl)
        yes = Button(text="Yes", size_hint=(1,.4)); yes.bind(on_release=func); displist.append(yes)
        no =  Button(text="No", size_hint=(1,.5)); no.bind(on_release=self.scrMain); displist.append(no)

        for widg in displist:
            self.add_widget(widg)
        debug("areYouSure() end", "title")

    def save(self, obj=None):
        debug("save()", "title")
        db = sqlite3.connect("rounddat.db") #connect to local db
        d = self.team.getAttr() #get information dict from self.team
        debug(d)
        db.execute("UPDATE `main` SET `highgoal`=?,`lowgoal`=?,`gears`=?,`Foul`=?,`TFoul`=?,`pickupGears`=?,`pickupBalls`=?,`climbed`=?,`capacity`=?,`aHighgoal`=?,`aLowgoal`=?,`aGears`=?,`scouterName`=?,`aCrossed`=?, `team color`=?, `AtpGears`=?, `MissHighGoal`=?, `notes`=?, `position`=?, `AGear Pos`=? WHERE `team`=? AND `round`=? AND `event`=?;",
                   (d["highgoal"],d["lowgoal"],d["gears"],d["Foul"],d["TFoul"],d["pickupGears"],d["pickupBalls"],d["climb"],d["capacity"],d["aHighgoal"],d["aLowgoal"],d["gfin"],d["scouterName"],d["aCrossed"],d["color"],d["AtpGears"],d["MissHighGoal"],d["prevnotes"],d["posfin"],self.rmapping[d["wg"]],d["number"],d["round"],CURRENT_EVENT)
                   ) #sql wizardry, simply takes out all of the stuff stored in d (data) and puts it in its respective places
        db.execute("UPDATE `team` SET `capacity`=?,`pickupGears`=?,`pickupBalls`=? WHERE `team`=?",
                   (d["capacity"],d["pickupGears"],d["pickupBalls"], self.team.number)) #updating the constants storage table
        c = db.cursor()
        c.execute("SELECT * FROM `main` WHERE `round`=? AND `team`=? AND `event`=?", (self.team.round, self.team.number, CURRENT_EVENT)) #just to check
        debug(c.fetchone())
        db.commit()
        db.close()
        self.didSave = "Saved." #switch button text
        debug("save() end", "title")
        self.scrExit()

    def uploadAll(self, obj=None): #uploads all data in the local database into the pi database
        debug("uploadAll()", "title")
        try:
            db = mysql.connector.connect(host=piip, user="pi", passwd="pi", db="matchdat") #connect to pi
        except:
            debug("unable to connect to database, aborting upload")
            self.didUploadAll = "Failed to connect to the database."
            self.scrExit()
            return
        dbl = sqlite3.connect("rounddat.db")
        cl = dbl.cursor()
        cl.execute("SELECT team, round, scouterName FROM `main`")
        fetchall = cl.fetchall()
        debug(fetchall)
        for fetchone in fetchall:
            debug(fetchone[0])
            debug(fetchone[1])
            self.setTeam(fetchone[0], fetchone[1], fetchone[2])
            self.upload()
        self.didUploadAll = "Uploaded."
        cl.close()
        dbl.close()
        debug("uploadAll() end", "title")

    def download(self, obj=None): #TODO: implement
        debug("download()", "title")
        db = mysql.connector.connect(host=piip, user="pi", passwd="pi", db="matchdat")
        c = db.cursor()
        dbl = sqlite3.connect("rounddat.db")
        cl = dbl.cursor()
        c.execute("SELECT scouterName, gears, Foul, TFoul, highgoal, lowgoal, capacity, pickupBalls, pickupGears, aHighgoal, aLowgoal, aGears, aCrossed, climbed, `team color`, AtpGears, MissHighGoal, notes, position, team, round, event FROM `main` WHERE `round`=? AND `team`=? AND `event`=?", (self.team.round, self.team.number, CURRENT_EVENT))
        data = c.fetchone()

    def upload(self, obj=None): #uploads loaded data into the pi database
        debug("upload()", "title")
        try:
            db = mysql.connector.connect(host=piip, user="pi", passwd="pi", db="matchdat") #connect to pi
        except:
            debug("unable to connect to database, aborting upload")
            self.didUpload = "Failed to connect to the database"
            self.scrExit()
            return
        c = db.cursor(buffered=True)
        dbl = sqlite3.connect("rounddat.db") #connect to local db
        cl = dbl.cursor()

        cl.execute("SELECT scouterName, gears, Foul, TFoul, highgoal, lowgoal, capacity, pickupBalls, pickupGears, aHighgoal, aLowgoal, aGears, aCrossed, climbed, `team color`, atpGears, MissHighGoal, notes, position, team, round, event FROM `main` WHERE `round`=? AND `team`=? AND `event`=?", (self.team.round, self.team.number, CURRENT_EVENT))
        fetchoneList = list(cl.fetchone()) #grabbing all data from that giant sql statement above
        cl.execute("SELECT * FROM `main`")
        fetchall = cl.fetchall()
        fetchone = None
        for tup in fetchall: #workaround for a bug i was getting on the commented line below
            debug("Target round: %s, number: %s, event: %s" % (self.team.round, self.team.number, CURRENT_EVENT))
            debug("Actual round: %s, number: %s, event: %s" % (tup[0], tup[1], tup[3]))
            if tup[0] == self.team.round and tup[1] == self.team.number and tup[3] == CURRENT_EVENT:
                debug("whoag they match, breaking")
                fetchone = tup
                break
        #next line used to reorder all values that it was getting from the database, but was replaced with SELECT *
        cl.execute("SELECT * FROM `main` WHERE `round`=? AND `team`=? AND `event`=?", (self.team.round, self.team.number, CURRENT_EVENT))
        if not fetchone:
            fetchone = cl.fetchone()
        debug(fetchone)
        #i was dumb and was taking a strange ordering from the above cl.execute. it changed and then i had to reorder all the compatTableau values
        #it was easier to reorder them than to reformat the compatTableau, so this next line happens
        fetchone = list(fetchone)
        compatOrder = [fetchone[2]] + fetchone[4:] + [fetchone[1], fetchone[0], fetchone[3]]
        debug("compatTableau gets " + str(compatOrder))
        #self.compatTableau(c, compatOrder)
        fetchoneList = list(fetchone) #IF THIS ERRORS THE PROGRAM COULD NOT FIND THE CORRECT DATA TO UPLOAD
        debug("fetchoneList: "+str(fetchoneList))

        c.execute("SELECT * FROM `main` WHERE `team`=%s AND `round`=%s AND `event`=%s", (self.team.number, self.team.round, CURRENT_EVENT))
        test = c.fetchone()
        if not test: #setting up pi database to take the data
            c.execute("INSERT INTO `main`(`team`,`round`,`event`) VALUES (%s,%s,%s);", (self.team.number, self.team.round, CURRENT_EVENT))
        elif test: #if the pi database is already set to take the data
            debug("THERE SHOULD BE DATA HERE: " + str(test))

        orderFetch = [fetchoneList[2]] + fetchoneList[4:] + [fetchoneList[1]] + [fetchoneList[0]] + [fetchoneList[3]]
        debug(orderFetch)

        c.execute("""UPDATE `main` SET
                     `scouterName`=%s,
                     `gears`=%s,
                     `highgoal`=%s,
                     `lowgoal`=%s,
                     `capacity`=%s,
                     `pickupBalls`=%s,
                     `pickupGears`=%s,
                     `aHighgoal`=%s,
                     `aLowgoal`=%s,
                     `aGears`=%s,
                     `aCrossed`=%s,
                     `climbed`=%s,
                     `team color`=%s,
                     `AtpGears`=%s,
                     `MissHighGoal`=%s,
                     `notes`=%s,
                     `position`=%s,
                     `Foul`=%s,
                     `TFoul`=%s,
                     `AGear Pos`=%s
                     WHERE `team`=%s AND `round`=%s AND `event`=%s;""",
                  orderFetch
                  ) #send the pi the data
        d = self.team.getAttr()
        c.execute("SELECT * FROM `team` WHERE `team`=%s", (self.team.number,)) #get the constants table
        if not c.fetchone():
            c.execute("INSERT INTO `team`(`team`) VALUES (%s);", (self.team.number,)) #make it if it doesn't exist
        c.execute("UPDATE `team` SET `capacity`=%s,`pickupBalls`=%s,`pickupGears`=%s WHERE `team`=%s",
                  (d['capacity'],d["pickupGears"],d["pickupBalls"],d['number'])
                  ) #set the constants for the team

        c.execute("SELECT * FROM `main` WHERE `team`=%s AND `round`=%s AND `event`=%s", (fetchoneList[-3], fetchoneList[-2], fetchoneList[-1])) #test to see if data actually got there
        debug(c.fetchone())
        db.commit()
        c.close()
        db.close()
        cl.close()
        dbl.close()
        self.didUpload = "Uploaded."
        debug("upload() end")
        self.scrExit()

    def compatTableau(self, c, d, mode="INSERT"):
        debug("compatTableau", "title")
        c.execute("""CREATE TABLE IF NOT EXISTS `tableau` (
                     `team` INTEGER,
                     `round` INTEGER,
                     `event` TEXT,
                     `phase` TEXT,
                     `action` TEXT,
                     `successes` INTEGER,
                     `misses` INTEGER,
                     `accuracy` INTEGER,
                     `score` INTEGER
                     )""")
        debug(d)
        #order:
        #0 scoutername
        debug("gears        "+str(d[1]))
        debug("highgoal     "+str(d[2]))
        debug("lowgoal      "+str(d[3]))
        #4 capacity, 5 pickupBalls, 6 pickupGears
        debug("aHighgoal    "+str(d[7]))
        debug("aLowgoal     "+str(d[8]))
        #9 aGears, 10 aCrossed
        debug("climbed      "+str(d[11]))
        #12 team color
        debug("AtpGears     "+str(d[13]))
        debug("MissHighGoal "+str(d[14]))
        #15 notes, 16 Foul, 17 TFoul, 18 position
        debug("team         "+str(d[19]))
        debug("round        "+str(d[20]))
        debug("event        "+str(d[21]))

        try: accuracy = int((d[2]/(d[2]+d[14]))*100)
        except ZeroDivisionError: accuracy = 0
        c.execute("SELECT * FROM `tableau` WHERE team=%s AND round=%s AND event=%s", (d[19], d[20], d[21]))
        if c.fetchone():
            mode = "UPDATE `tableau` SET team=%s, round=%s, event=%s, phase=%s, action=%s, successes=%s, misses=%s, accuracy=%s, score=%s WHERE team=%s AND round=%s AND event=%s"
            appendix = [d[19], d[20], d[21]]
        else:
            mode = "INSERT INTO tableau (team, round, event, phase, action, successes, misses, accuracy, score) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            appendix = [ ]
        debug(mode )

        c.execute(mode, [d[19], d[20], d[21], "teleop", "highgoal", d[2], d[14], accuracy, int(d[2]/3)] + appendix)
        c.execute(mode, [d[19], d[20], d[21], "teleop", "lowgoal", d[3], 0, 100, int(d[3]/9)] + appendix)
        misses = d[13] - d[1]
        try: accuracy = int((d[1]/d[13])*100)
        except ZeroDivisionError: accuracy = 0
        c.execute(mode, [d[19], d[20], d[21], "teleop", "gears", d[1], misses, accuracy, int(d[1])] + appendix)
        c.execute(mode, [d[19], d[20], d[21], "teleop", "climbed", d[11], int(not d[11]), d[11]*100, d[11]*50] + appendix)
        c.execute(mode, [d[19], d[20], d[21], "auton", "highgoal", d[7], 0, 0, int(d[7])] + appendix)
        c.execute(mode, [d[19], d[20], d[21], "auton", "lowgoal", d[8], 0, 0, int(d[8]/3)] + appendix)
        c.execute(mode, [d[19], d[20], d[21], "auton", "gears", d[9], 0, 0, int(d[9])] + appendix)
        c.execute(mode, [d[19], d[20], d[21], "auton", "crossed line", d[10], int(not d[10]), 0, d[10]*10] + appendix)

        #copy paste these when adding values

        debug("compatTableau end", "title")

#lsl - 15.5, ll - 23, ssl - 7.75, sl - 11.5
#sea foam green: , rgb=[(14/255),(201/255),(170/255)] :  low goal
#dark magenta:   , rgb=[(201/255),(28/255),(147/255)] :  climbed, capab
#fair blue:      , rgb=[(28/255),(129/255),(201/255)] :  gears
#happy green:    , rgb=[(28/255),(201/255),(40/255)] :   high goal
#fair orange:    , rgb=[(201/255),(170/255),(28/255)] :  switch
#black:          , rgb=[0, 0, 0, 1] :                    title
#blue:           , rgb=[(25/255), 0, 0] :                team blue
#red:            , rgb=[0, 0, (25/255)] :                team red

class MyApp(App):
    def build(self):
        return Screen()


if __name__ == "__main__":
    MyApp().run()

#wha-pang
#boioioioioiioioioioioioioioioioioioioioioioioing

#hard instantly
