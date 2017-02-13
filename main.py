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

import sqlite3
import mysql.connector

import os

#mysql pi ip: 10.111.49.41

DEBUG = 1
def debug(msg):
    if DEBUG:
        print("[hol up] " + str(msg))

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
""")
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

#the following functions are for decluttering the scr functions
def smallButton(txt, rgb=[.5,.5,.5], height=.1666666666666667):
    return cButton(text=txt, rgb=rgb, size_hint=(.115, height))
def smallLabel(txt, rgb=[.5,.5,.5], height=.1666666666666667):
    return cLabel(text=txt, rgb=rgb, size_hint=(.115, height))

def smallSideButton(txt, rgb=[.5,.5,.5], height=.1666666666666667):
    return cButton(text=txt, rgb=rgb, size_hint=(.0775, height))
def smallSideLabel(txt, rgb=[.5,.5,.5], height=.1666666666666667):
    return cLabel(text=txt, rgb=rgb, size_hint=(.0775, height))

def largeButton(txt, rgb=[.5,.5,.5], height=.1666666666666667):
    return cButton(text=txt, rgb=rgb, size_hint=(.23, height))
def largeLabel(txt, rgb=[.5,.5,.5], height=.1666666666666667):
    return cLabel(text=txt, rgb=rgb, size_hint=(.23, height))

def largeSideButton(txt, rgb=[.5,.5,.5], height=.1666666666666667):
    return cButton(text=txt, rgb=rgb, size_hint=(.155, height))
def largeSideLabel(txt, rgb=[.5,.5,.5], height=.1666666666666667):
    return cLabel(text=txt, rgb=rgb, size_hint=(.155, height))

def autonLabel(txt, rgb=[.5, .5, .5]):
    return cLabel(text=str(txt), rgb=rgb, size_hint=((1/3), (1/6)))
def autonButton(txt, rgb=[.5, .5, .5]):
    return cButton(text=str(txt), rgb=rgb, size_hint=((1/3), (1/6)))

class Team:
    def __init__(self, number):
        self.number = number
        self.highgoal = 0
        self.lowgoal = 0
        self.gears = 0
        self.climb = 0

        self.pickupGears = 0
        self.pickupBalls = 0
        self.capacity = 0
        self.AptGears = 0
        self.MissHighGoal = 0
        self.prevnotes = ''
        self.posfin = 1
        self.tog = 'boiler'
        self.togcolor = [(117/255), (117/255), (117/255)]

        self.aHighgoal = 0
        self.aLowgoal = 0
        self.aGears = 0
        self.aCrossed = 0
        self.color = True

    def getAttr(self):
        return vars(self)

    def putData(self, c):
        c.execute("SELECT * FROM `main` WHERE `team`=? AND `round`=? AND `event`=?", (self.number, self.round, self.event))
        data = list(c.fetchone())
        for i in range(len(data)):
            if data[i] == None:
                data[i] = 0
        print(str(len(data)))
        try:
            self.gears=data[4]; self.highgoal=data[5]; self.lowgoal=data[6]; self.climb=data[14]; self.capacity=data[7]; self.pickupBalls=data[8]; self.pickupGears=data[9]
            self.aLowgoal=data[11]; self.aHighgoal=data[10]; self.aGears=data[12]; self.aCrossed=data[13]; self.color=data[15]; debug('working'); self.AptGears=data[16]; self.MissHighGoal=data[17]
            self.prevnotes=data[18]; self.posfin=data[19]
        except:
            debug("whoops, putdata got an error")
            debug("heres data stuff: %s" % data)

        c.execute("SELECT * FROM `team` WHERE `team`=?", (self.number))
        data = c.fetchone()
        if data:
            data = list(data)
            for i in range(len(data)):
                if data[i] == None:
                    data[i] = 0
        try:
            self.capacity=data[1]
        except:
            debug('ok')

class Screen(StackLayout):
    prev = ''
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.lastLowVal = 0
        self.choose()
        self.reloadList = list()

    def makeDB(self, db):
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
                                                        `AptGears` INTEGER,
                                                        `MissHighGoal` INTEGER,
                                                        `notes` TEXT,
                                                        `position` INTEGER,
                                                        PRIMARY KEY(`team`,`round`))''')
        db.execute("CREATE TABLE IF NOT EXISTS `lastscouter` (`name` TEXT)")
        debug("makeDB was called")
        db.execute('''CREATE TABLE IF NOT EXISTS `team`(
                                                        `team`INTEGER NOT NULL,
                                                        `capacity` INTEGER,
                                                        PRIMARY KEY(`team`))''')

    def getlastscouter (self, defalt=''):
        db = sqlite3.connect('rounddat.db')
        self.makeDB(db)
        pos = db.cursor()
        res = pos.execute('SELECT * FROM lastscouter')
        row = pos.fetchone()
        pos.close()
        db.close()
        if row == None:
            return defalt
        else:
            return row[0]

    def setlastscouter (self, name):
        print(name)
        if self.getlastscouter(None) == None:
            scouterexist = False
        else:
            scouterexist = True
        db = sqlite3.connect ('rounddat.db')
        if scouterexist:
            db.execute("UPDATE `lastscouter` SET `name`=?", (name,))
        else:
            db.execute("INSERT INTO `lastscouter`(`name`) VALUES (?);", (name,))
        db.commit()
        db.close()

    def choose(self, hint="", obj=None):
        self.clear_widgets()
        displist = list()

        displist.append(cLabel(rgb=[(14/255),(201/255),(170/255)], text="Enter team number:", size_hint=(.5, .25)))
        self.teamsel =  TextInput(hint_text=hint,multiline=False,size_hint=(.5, .25))
        displist.append(self.teamsel)

        displist.append(cLabel(rgb=[(14/255),(201/255),(170/255)], text="Enter round number:", size_hint=(.5, .25)))
        self.roundsel = TextInput(hint_text=hint, multiline=False, size_hint=(.5, .25))
        displist.append(self.roundsel)

        displist.append(cLabel(rgb=[(14/255),(201/255),(170/255)], text="Enter your full name:", size_hint=(.5, .25)))
        self.name = TextInput(multiline=False, size_hint=(.5, .25), text=self.getlastscouter())
        displist.append(self.name)

        gobutton = cButton(text="Go", size_hint=(1, .25), padding=[10,10]); displist.append(gobutton)
        self.name.bind(on_text_validate=self.pressGo)
        gobutton.bind(on_release=self.pressGo)

        for widg in displist:
            self.add_widget(widg)

    def pressGo(self, obj):
        if self.teamsel.text and self.roundsel.text:
            self.setTeam(self.teamsel.text, self.roundsel.text, self.name.text)
            self.setlastscouter(self.name.text)
        else:
            print("unable to setTeam, number %s, round %s" % (self.teamsel.text, self.roundsel.text))
            self.choose(hint="Enter a number value.")

    def setTeam(self, team, round, name): #TODO: integrate event key into code
        self.team = Team(team)
        self.team.round = round
        self.team.scouterName = name
        db = mysql.connector.connect(host="10.111.49.41", user="pi", passwd="pi", db="matchdat") #connect to pi
        c = db.cursor()
        c.execute("SELECT `currentEvent` FROM `events`")
        self.team.event = c.fetchone()[0]
        debug(self.team.event)
        self.team.prevnotes = ""


        dbl = sqlite3.connect("rounddat.db") #connect to local database
        cl = dbl.cursor()
        found = True
        try:
            cl.execute("SELECT * FROM `main` WHERE `round`=? AND `team`=?", (round, team))
            found = cl.fetchone()
        except:
            self.makeDB()
            found = False
            pass
        if not found:
            dbl.execute("INSERT INTO `main`(`round`,`team`,`scouterName`,`event`) VALUES (?,?,?,?);", (round, team, name, self.team.event))
            dbl.execute("UPDATE `main` SET `scouterName`=? WHERE `round`=? AND `team`=? AND `event`=?", (name, round, team, self.team.event))
            dbl.commit()
        else:
            self.team.putData(cl)
        debug(self.team.color)

        found = True

        cl.execute("SELECT * FROM `team` WHERE `team`=?", (team))
        found = cl.fetchone()
        if not found:
            dbl.execute("INSERT INTO `team`(`team`) VALUES (?);", (team))
            dbl.commit()


        #color
        if self.team.color == None:
            self.team.color = True
        elif self.team.color == 1:
            self.team.color == True
        else:
            self.team.color = False

        if self.team.color == False:
            debug('hi')
            self.buttoncolor = [(200/255), 0, 0]
        else:
            self.buttoncolor =[0, 0,(200/255)]
        #position
        if self.team.posfin == 1:
            self.team.tog = 'boliler'
            self.team.togcolor = [(117/255), (117/255), (117/255)]
        elif self.team.posfin == 2:
            self.team.tog = 'middle'
            self.team.togcolor = [0, (255/255), (42/255)]
        else:
            self.team.tog = 'far'
            self.team.togcolor = [(235/255), (61/255), (255/255)]
        debug('this one')
        debug(self.team.posfin)
        debug('this one')

        debug(self.team.color)
        c.close()
        cl.close()
        db.close()
        dbl.close()
        self.scrMain()

    #the following functions are called by the buttons on the interface when pressed
    def addLow(self, count, widg):
        self.reloadList = [widg]
        self.team.lowgoal += count
        if self.team.lowgoal <= 0:
            self.team.lowgoal = 0
        widg.text = str(self.team.lowgoal)
    def addHigh(self, count, widg):
        self.reloadList = [widg]
        self.team.highgoal += count
        if self.team.highgoal <= 0:
            self.team.highgoal = 0
        widg.text = str(self.team.highgoal)
    def addMissHigh(self, count, widg):
        self.reloadList = [widg]
        self.team.MissHighGoal += count
        if self.team.MissHighGoal <= 0:
            self.team.MissHighGoal = 0
        widg.text = str(self.team.MissHighGoal)
    def addGear(self, count, widg):
        self.reloadList = [widg]
        self.team.gears += count
        if self.team.gears <= 0:
            self.team.gears = 0
        widg.text = str(self.team.gears)
    def addAptGear(self, count, widg):
        self.reloadList = [widg]
        self.team.AptGears += count
        if self.team.AptGears <= 0:
            self.team.AptGears = 0
        widg.text = str(self.team.AptGears)
    def canPickGear(self, widg, obj=None):
        self.reloadList = [widg]
        self.team.pickupGears = int(not self.team.pickupGears)
        widg.text = "The robot %s pickup gears off of the ground." % ("CAN" if self.team.pickupGears else "CAN'T")
    def canPickBall(self, widg, obj=None):
        self.reloadList = [widg]
        self.team.pickupBalls = int(not self.team.pickupBalls)
        widg.text = "The robot %s pickup balls off of the ground." % ("CAN" if self.team.pickupBalls else "CAN'T")
    def climbed(self, widg, obj=None):
        self.reloadList = [widg]
        self.team.climb = int(not self.team.climb)
        widg.text = "yes" if self.team.climb else "no"
    def color(self, widg, obj=None):
        self.reloadList = [widg]
        self.team.color = int(not self.team.color)
        debug('color run')
        if self.team.color:
            self.buttoncolor = [0, 0, (200/255)]
        else:
            self.buttoncolor =[(200/255), 0, 0]
        self.scrMain()
    def aAddLow(self, count, widg):
        self.reloadList = [widg]
        self.team.aLowgoal += count
        if self.team.aLowgoal <= 0:
            self.team.aLowgoal = 0
        widg.text = str(self.team.aLowgoal)
    def aAddHigh(self, count, widg):
        self.reloadList = [widg]
        self.team.aHighgoal += count
        if self.team.aHighgoal <= 0:
            self.team.aHighgoal = 0
        widg.text = str(self.team.aHighgoal)
    def aAddGear(self, widg, obj=None):
        self.reloadList = [widg]
        self.team.aGears = int(not self.team.aGears)
        widg.text = "The team %s use their gear."%("DID"if self.team.aGears else"DIDN'T")
    def aToggleCross(self, widg, obj=None):
        self.reloadList = [widg]
        self.team.aCrossed = int(not self.team.aCrossed)
        widg.text = "The team %s cross the ready line."%("DID"if self.team.aCrossed else"DIDN'T")
    def checkpos(self, widg):
        self.reloadList = [widg]
        self.team.posfin = self.team.posfin + 1
        debug(self.team.posfin)
        if self.team.posfin >= 3:
            self.team.posfin = self.team.posfin - 3
        if self.team.posfin == 1:
            self.team.tog = 'boiler'
            self.team.togcolor = [(117/255), (117/255), (117/255)]
        elif self.team.posfin == 2:
            self.team.tog = 'middle'
            self.team.togcolor = [0, (255/255), (42/255)]
        else:
            self.team.tog = 'far'
            self.team.togcolor = [(235/255), (61/255), (255/255)]
        self.scrMain()

    #main functions (displays)
    def scrMain(self, obj=None, reload=False): #used for teleop
        displist = list()
        self.camefrom = "tele"
        self.didSave = "Save" #reset menu button text
        self.didUpload = "Upload (Save before uploading)"

            #line 1
        lowLbl =       largeSideLabel("Low goal", rgb=[(14/255),(201/255),(170/255)]); displist.append(lowLbl)
        dummyLbl =     cLabel(text="Event " + str(self.team.event), rgb=[0, 0, 0, 1], size_hint=(.23, .075)); displist.append(dummyLbl)
        teamDisp =     largeLabel("Team " + str(self.team.number), rgb=[0, 0, 0, 1]); displist.append(teamDisp)
        dummyLbl2 =    cLabel(text="Scouter " + str(self.team.scouterName), rgb=[0, 0, 0, 1], size_hint=(.23, .075)); displist.append(dummyLbl2)
        highLbl =      largeSideLabel("High goal\n\nHit     Miss", rgb=[(28/255),(201/255),(40/255)]); displist.append(highLbl)

            #line 2
        lowDisp =      largeSideLabel(str(self.team.lowgoal), rgb=[(14/255),(201/255),(170/255)]); displist.append(lowDisp)
        checkColor =  smallButton("Team Blue" if self.team.color else "Team Red", rgb=self.buttoncolor); checkColor.bind(on_release=lambda x: self.color(checkColor)); displist.append(checkColor)
        checkpos = smallButton(self.team.tog, self.team.togcolor); checkpos.bind(on_release=lambda x: self.checkpos(checkpos)); displist.append(checkpos)
        '''dummyLbl51 =   smallButton("", rgb=[0, (255/255), (42/255)]); displist.append(dummyLbl51)'''
        dummyLbl4 =    largeLabel("Teleop", rgb=[0, 0, 0, 1]); displist.append(dummyLbl4)
        toggleExit =   largeButton("Menu", rgb=[(201/255),(170/255),(28/255)]); toggleExit.bind(on_release=self.scrExit); displist.append(toggleExit)
        highDisp =     smallSideLabel(str(self.team.highgoal), rgb=[(28/255),(201/255),(40/255)]); displist.append(highDisp)
        MissHighDisp = smallSideLabel(str(self.team.MissHighGoal), rgb=[(120/255),(201/255),(40/255)]); displist.append(MissHighDisp)

            #line 3
        incLow1 =      smallSideButton("-1", rgb=[(14/255),(201/255),(170/255)]); incLow1.bind(on_release=lambda x: self.addLow(-1, lowDisp)); displist.append(incLow1)
        incLow5 =      smallSideButton("-5", rgb=[(14/255),(201/255),(170/255)]); incLow5.bind(on_release=lambda x: self.addLow(-5, lowDisp)); displist.append(incLow5)
        capLbl =       largeLabel("Capacity", rgb=[(14/255),(201/255),(170/255)]); displist.append(capLbl)
        toggleAuton =  largeButton("Auton", rgb=[(201/255),(170/255),(28/255)]); toggleAuton.bind(on_release=self.scrAuton); displist.append(toggleAuton)
        toggleCapab =  largeButton("Capability", rgb=[(201/255),(170/255),(28/255)]); toggleCapab.bind(on_release=self.scrCapab); displist.append(toggleCapab)
        decHigh =      smallSideButton("-1", rgb=[(28/255),(201/255),(40/255)]); decHigh.bind(on_release=lambda x: self.addHigh(-1, highDisp)); displist.append(decHigh)
        decMissHigh =  smallSideButton("-1", rgb=[(120/255),(201/255),(40/255)]); decMissHigh.bind(on_release=lambda x: self.addMissHigh(-1, MissHighDisp)); displist.append(decMissHigh)

            #line 4
        incLow10 =     smallSideButton("-10", rgb=[(14/255),(201/255),(170/255)]); incLow10.bind(on_release=lambda x: self.addLow(-10, lowDisp)); displist.append(incLow10)
        incLow20 =     smallSideButton("-20", rgb=[(14/255),(201/255),(170/255)]); incLow20.bind(on_release=lambda x: self.addLow(-20, lowDisp)); displist.append(incLow20)
        capDispAdd =   smallButton("+" + str(self.team.capacity), rgb=[(14/255),(201/255),(170/255)]); capDispAdd.bind(on_release=lambda x: self.addLow(self.team.capacity, lowDisp)); displist.append(capDispAdd)
        capDispSub =   smallButton("-" + str(self.team.capacity), rgb=[(14/255),(201/255),(170/255)]); capDispSub.bind(on_release=lambda x: self.addLow(-self.team.capacity, lowDisp)); displist.append(capDispSub)
        toggleTeam =   largeButton("Team", rgb=[(201/255),(170/255),(28/255)]); toggleTeam.bind(on_release=self.areYouSure); displist.append(toggleTeam)
        togglenotes =  largeButton("Notes", rgb=[(201/255),(170/255),(28/255)]); togglenotes.bind(on_release=self.scrnotes); displist.append(togglenotes)
        '''dummyLbl10 =   largeLabel("", rgb=[(201/255),(170/255),(28/255)]); displist.append(dummyLbl10)'''
        addHigh1 =     smallSideButton("-3", rgb=[(28/255),(201/255),(40/255)]); addHigh1.bind(on_release=lambda x: self.addHigh(-3, highDisp)); displist.append(addHigh1)
        addMissHigh1 = smallSideButton("-3", rgb=[(120/255),(201/255),(40/255)]); addMissHigh1.bind(on_release=lambda x: self.addMissHigh(-3, MissHighDisp)); displist.append(addMissHigh1)

            #line 5
        decLow1 =      smallSideButton("1", rgb=[(14/255),(201/255),(170/255)]); decLow1.bind(on_release=lambda x: self.addLow(1, lowDisp)); displist.append(decLow1)
        decLow5 =      smallSideButton("5", rgb=[(14/255),(201/255),(170/255)]); decLow5.bind(on_release=lambda x: self.addLow(5, lowDisp)); displist.append(decLow5)
        climbLbl =     largeLabel("Climbed", rgb=[(201/255),(28/255),(147/255)]); displist.append(climbLbl)
        gearLbl =      smallLabel("Gears", rgb=[(28/255),(129/255),(201/255)]); displist.append(gearLbl)
        gearDisp =     smallLabel(str(self.team.gears), rgb=[(28/255),(129/255),(201/255)]); displist.append(gearDisp)
        AptGearLbl =   smallLabel("Miss Gears", rgb=[(28/255),0,(201/255)]); displist.append(AptGearLbl)#AptGears is the varible for Miss Gears
        AptGearDisp =  smallLabel(str(self.team.AptGears), rgb=[(28/255),0,(201/255)]); displist.append(AptGearDisp)
        addHigh2 =     smallSideButton("+1", rgb=[(28/255),(201/255),(40/255)]); addHigh2.bind(on_release=lambda x: self.addHigh(1, highDisp)); displist.append(addHigh2)
        addMissHigh2 = smallSideButton("+1", rgb=[(120/255),(201/255),(40/255)]); addMissHigh2.bind(on_release=lambda x: self.addMissHigh(1, MissHighDisp)); displist.append(addMissHigh2)

            #line 6
        decLow10 =     smallSideButton("10", rgb=[(14/255),(201/255),(170/255)]); decLow10.bind(on_release=lambda x: self.addLow(10, lowDisp)); displist.append(decLow10)
        decLow20 =     smallSideButton("20", rgb=[(14/255),(201/255),(170/255)]); decLow20.bind(on_release=lambda x: self.addLow(20, lowDisp)); displist.append(decLow20)
        checkClimb =   largeButton("yes" if self.team.climb else "no", rgb=[(201/255),(28/255),(147/255)]); checkClimb.bind(on_release=lambda x: self.climbed(checkClimb)); displist.append(checkClimb)
        addGear =      smallButton("+", rgb=[(28/255),(129/255),(201/255)]); addGear.bind(on_release=lambda x: self.addGear(1, gearDisp)); displist.append(addGear)
        decGear =      smallButton("-", rgb=[(28/255),(129/255),(201/255)]); decGear.bind(on_release=lambda x: self.addGear(-1, gearDisp)); displist.append(decGear)
        addAptGear =   smallButton("+", rgb=[(28/255),0,(201/255)]); addAptGear.bind(on_release=lambda x: self.addAptGear(1, AptGearDisp)); displist.append(addAptGear)
        decAptGear =   smallButton("-", rgb=[(28/255),0,(201/255)]); decAptGear.bind(on_release=lambda x: self.addAptGear(-1, AptGearDisp)); displist.append(decAptGear)
        addHigh3 =     smallSideButton("+3", rgb=[(28/255),(201/255),(40/255)]); addHigh3.bind(on_release=lambda x: self.addHigh(3, highDisp)); displist.append(addHigh3)
        addMissHigh3 = smallSideButton("+3", rgb=[(120/255),(201/255),(40/255)]); addMissHigh3.bind(on_release=lambda x: self.addMissHigh(3, MissHighDisp)); displist.append(addMissHigh3)

        if not reload:
            self.clear_widgets()
            for widg in displist:
                self.add_widget(widg)
        else:
            for widg in self.reloadList:
                self.remove_widget(widg)
                self.add_widget(widg)

    def scrExit(self, obj=None):
        self.clear_widgets()
        displist = list()
        self.camefrom = "exit"
        #row 1
        cancel =   Button(text="Cancel", size_hint=(1,.1)); cancel.bind(on_release=self.scrMain); displist.append(cancel)
        #row 2
        saveExit = Button(text=self.didSave, size_hint=(.34,.8)); saveExit.bind(on_release=self.save); displist.append(saveExit)
        upload = Button(text=self.didUpload, size_hint=(.33,.8)); upload.bind(on_release=self.upload); displist.append(upload)
        Team = Button(text="Team", size_hint=(.33,.8)); Team.bind(on_release=lambda x: self.areYouSure("tele")); displist.append(Team)
        #row 3
        exit =     Button(text="Exit", size_hint=(1, .1)); exit.bind(on_release=lambda x: self.areYouSure("exit")); displist.append(exit)

        for widg in displist:
            self.add_widget(widg)

    def scrCapab(self, obj=None, cap=None, reload=False):
        displist = list()
        capChangeText = ""
        if not cap == None:
            try:
                self.team.capacity = int(cap)
            except:
                capChangeText = "Enter a number value."

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

        if not reload:
            self.clear_widgets()
            for widg in displist:
                self.add_widget(widg)
        else:
            for widg in self.reloadList:
                self.remove_widget(widg)
                self.add_widget(widg)

    def savednotes(self, notesfield):
        self.team.prevnotes = notesfield.text
        debug('-----notes-----')
        debug(self.team.prevnotes)
        debug(notesfield.text)
        self.scrMain()

    def scrnotes(self, obj=None, cap=None):
        self.clear_widgets()
        displist = list()
        notesText = self.team.prevnotes

        #row 1
        cancel = cButton(text="Cancel", size_hint=(1, .1)); cancel.bind(on_release=self.scrMain if self.camefrom == "tele" else self.scrAuton); displist.append(cancel)
        #row 2
        notes = TextInput(text=self.team.prevnotes, multiline=True, size_hint=(1, .8)); notes.bind(on_text_validate=lambda x: self.scrnotes); displist.append(notes)
        #row 3
        save = cButton(text="Save", size_hint=(1, .1)); save.bind(on_release=lambda x: self.savednotes(notes)); displist.append(save)

        for widg in displist:
            self.add_widget(widg)

    def scrAuton(self, obj=None, reload=False):
        displist = list()
        self.reloadlist = list()
        self.camefrom = "auton"

        #row 1
        lowLbl =  autonLabel(txt="Low", rgb=[(14/255),(201/255),(170/255)]); displist.append(lowLbl)
        teamLbl = autonLabel(txt=self.team.number, rgb=[0, 0, 0, 1]); displist.append(teamLbl)
        highLbl = autonLabel(txt="High", rgb=[(28/255),(201/255),(40/255)]); displist.append(highLbl)
        #row 2
        lowDisp =  autonLabel(txt=self.team.aLowgoal, rgb=[(14/255),(201/255),(170/255)]); displist.append(lowDisp)
        autonLbl = autonLabel(txt="Auton", rgb=[0, 0, 0, 1]); displist.append(autonLbl)
        highDisp = autonLabel(txt=self.team.aHighgoal, rgb=[(28/255),(201/255),(40/255)]); displist.append(highDisp)
        #row 3
        low1 =       autonButton(txt="+1", rgb=[(14/255),(201/255),(170/255)]); low1.bind(on_release=lambda x: self.aAddLow(1, lowDisp)); displist.append(low1)
        toggleTele = autonButton(txt="Teleop", rgb=[(201/255),(170/255),(28/255)]); toggleTele.bind(on_release=self.scrMain); displist.append(toggleTele)
        high1 =      autonButton(txt="+1", rgb=[(28/255),(201/255),(40/255)]); high1.bind(on_release=lambda x: self.aAddHigh(1, highDisp)); displist.append(high1)
        #row 4
        low5 =        autonButton(txt="+5", rgb=[(14/255),(201/255),(170/255)]); low5.bind(on_release=lambda x: self.aAddLow(5, lowDisp)); displist.append(low5)
        toggleCapab = autonButton(txt="Capability", rgb=[(201/255),(170/255),(28/255)]); toggleCapab.bind(on_release=self.scrCapab); displist.append(toggleCapab)
        high3 =       autonButton(txt="+3", rgb=[(28/255),(201/255),(40/255)]); high3.bind(on_release=lambda x: self.aAddHigh(3, highDisp)); displist.append(high3)
        #row 5
        lowm1 =   autonButton(txt="-1", rgb=[(14/255),(201/255),(170/255)]); lowm1.bind(on_release=lambda x: self.aAddLow(-1, lowDisp)); displist.append(lowm1)
        gearBtn = autonButton(txt="The team %s use their gear."%("DID"if self.team.aGears else"DIDN'T"),rgb=[(28/255),(129/255),(201/255)]);gearBtn.bind(on_release=self.aAddGear);displist.append(gearBtn)
        highm1 =  autonButton(txt="-1", rgb=[(28/255),(201/255),(40/255)]); highm1.bind(on_release=lambda x: self.aAddHigh(-1, highDisp)); displist.append(highm1)
        #row 6
        lowm5 =  autonButton(txt="-5", rgb=[(14/255),(201/255),(170/255)]); lowm5.bind(on_release=lambda x: self.aAddLow(-5, lowDisp)); displist.append(lowm5)
        xedBtn = autonButton(txt="The team %s cross the ready line."%("DID"if self.team.aCrossed else"DIDN'T"),rgb=[(28/255),(129/255),(201/255)]);xedBtn.bind(on_release=self.aToggleCross);displist.append(xedBtn)
        highm3 = autonButton(txt="-3", rgb=[(28/255),(201/255),(40/255)]); highm3.bind(on_release=lambda x: self.aAddHigh(-3, highDisp)); displist.append(highm3)

        if not reload:
            self.clear_widgets()
            for widg in displist:
                self.add_widget(widg)
        else:
            for widg in self.reloadList:
                self.remove_widget(widg)
                self.add_widget(widg)

    def areYouSure(self, camefrom=None, obj=None):
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

    def save(self, obj=None):
        debug("save function")
        db = sqlite3.connect("rounddat.db") #connect to local db
        d = self.team.getAttr() #get information dict from self.team
        debug(d)
        db.execute("UPDATE `main` SET `highgoal`=?,`lowgoal`=?,`gears`=?,`pickupGears`=?,`pickupBalls`=?,`climbed`=?,`capacity`=?,`aHighgoal`=?,`aLowgoal`=?,`aGears`=?,`scouterName`=?,`aCrossed`=?, `team color`=?, `AptGears`=?, `MissHighGoal`=?, `notes`=?, `position`=? WHERE `team`=? AND `round`=? AND `event`=?;",
                   (d["highgoal"],d["lowgoal"],d["gears"],d["pickupGears"],d["pickupBalls"],d["climb"],d["capacity"],d["aHighgoal"],d["aLowgoal"],d["aGears"],d["scouterName"],d["aCrossed"],d["color"],d["AptGears"],d["MissHighGoal"],d["prevnotes"],d["posfin"],d["number"],d["round"],d["event"])
                   )
        db.execute("UPDATE `team` SET `capacity`=? WHERE `team`=?",
                    (d["capacity"], self.team.number))
        c = db.cursor()
        c.execute("SELECT * FROM `main` WHERE `round`=? AND `team`=? AND `event`=?", (self.team.round, self.team.number, self.team.event)) #just to check
        debug(c.fetchone())
        db.commit()
        db.close()
        self.didSave = "Saved." #switch button text
        self.scrExit()

    def upload(self, obj=None):
        debug("upload function")
        db = mysql.connector.connect(host="10.111.49.41", user="pi", passwd="pi", db="matchdat") #connect to pi
        c = db.cursor()
        dbl = sqlite3.connect("rounddat.db") #connect to local db
        cl = dbl.cursor()
        cl.execute("SELECT scouterName, gears, highgoal, lowgoal, capacity, pickupBalls, pickupGears, aHighgoal, aLowgoal, aGears, aCrossed, climbed, `team color`, AptGears, MissHighGoal, notes, position, team, round, event FROM `main` WHERE `round`=? AND `team`=? AND `event`=?", (self.team.round, self.team.number, self.team.event))
        fetchone = list(cl.fetchone())
        fetchoneList = fetchone

        debug("fetchone:     "+str(fetchone))
        debug("fetchoneList: "+str(fetchoneList))
        c.execute("SELECT * FROM `main` WHERE `team`=%s AND `round`=%s AND `event`=%s", (self.team.round, self.team.number, self.team.event))
        if not c.fetchone():
            c.execute("INSERT INTO `main`(`team`,`round`,`event`) VALUES (%s,%s,%s);", (self.team.round, self.team.number, self.team.event))
        c.execute("UPDATE `main` SET `scouterName`=%s,`gears`=%s,`highgoal`=%s,`lowgoal`=%s,`capacity`=%s,`pickupBalls`=%s,`pickupGears`=%s,`aHighgoal`=%s,`aLowgoal`=%s,`aGears`=%s,`aCrossed`=%s,`climbed`=%s, `team color`=%s, `AptGears`=%s, `MissHighGoal`=%s, `notes`=%s, `position`=%s WHERE `team`=%s AND `round`=%s AND `event`=%s;",
                  fetchoneList
                  )
        d = self.team.getAttr()
        c.execute("SELECT * FROM `team` WHERE `team`=%s", (self.team.number,))
        if not c.fetchone():
            c.execute("INSERT INTO `team`(`team`) VALUES (%s);", (self.team.number,))
        c.execute("UPDATE `team` SET `capacity`=%s WHERE `team`=%s",
                  (d['capacity'],d['number'])
                  )

        c.execute("SELECT * FROM `main` WHERE `team`=%s AND `round`=%s AND `event`=%s", (fetchone[0], fetchone[1], fetchone[3]))
        debug(c.fetchone())
        db.commit()
        c.close()
        db.close()
        cl.close()
        dbl.close()
        self.didUpload = "Uploaded."
        self.scrExit()

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
#        if os.geteuid() != 0:
#            os.system("sudo main.py")
        return Screen()

if __name__ == "__main__":
    MyApp().run()
