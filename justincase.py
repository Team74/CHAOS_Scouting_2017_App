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
import random

#mysql pi ip: 10.111.49.41

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

#ascii table setup:
#                                         #
#-----------------------------------------#
#- - - - - - - - - - - - - - - - - - - - -#

#the following functions are for decluttering the scr functions     #---examples------------------------------#
#large button/label witdh div by 2                                  #-----------------------------------------#
def smallButton(txt, rgb=[.5,.5,.5], height=.1666666666666667):     # the add capacity to low goal buttons    #
    return cButton(text=txt, rgb=rgb, size_hint=(.115, height))     #-----------------------------------------#
def smallLabel(txt, rgb=[.5,.5,.5], height=.1666666666666667):
    return cLabel(text=txt, rgb=rgb, size_hint=(.115, height))
                                                                    #                                         #
#large side button/label width div by 2                             #-----------------------------------------#
def smallSideButton(txt, rgb=[.5,.5,.5], height=.1666666666666667): # low goal add and subtract buttons       #
    return cButton(text=txt, rgb=rgb, size_hint=(.0775, height))    #-----------------------------------------#
def smallSideLabel(txt, rgb=[.5,.5,.5], height=.1666666666666667):
    return cLabel(text=txt, rgb=rgb, size_hint=(.0775, height))     #                                         #
                                                                    #                                         #
#full size buttons and labels for the middle of the UI              #-----------------------------------------#
def largeButton(txt, rgb=[.5,.5,.5], height=.1666666666666667):     # gear add and subtract buttons           #
    return cButton(text=txt, rgb=rgb, size_hint=(.23, height))      #-----------------------------------------#
def largeLabel(txt, rgb=[.5,.5,.5], height=.1666666666666667):      # gear label, climb label, capacity label #
    return cLabel(text=txt, rgb=rgb, size_hint=(.23, height))       #-----------------------------------------#
                                                                    #                                         #
                                                                    #                                         #
#full size buttons and labels for the side of the UI                #                                         #
#large button not needed                                            #-----------------------------------------#
def largeSideLabel(txt, rgb=[.5,.5,.5], height=.1666666666666667):  # high/low goal label and disp            #
    return cLabel(text=txt, rgb=rgb, size_hint=(.155, height))      #-----------------------------------------#

#all buttons and labels in the auton screen
def autonLabel(txt, rgb=[.5, .5, .5]):
    return cLabel(text=str(txt), rgb=rgb, size_hint=((1/3), (1/6)))
def autonButton(txt, rgb=[.5,.5,.5]):
    return cButton(text=str(txt), rgb=rgb, size_hint=((1/3), (1/6)))

class Team:
    def __init__(self, number):
        #constants
        self.number = number
        self.highgoal = 0
        self.lowgoal = 0
        self.gears = 0
        #teleop
        self.climb = 0 #whether or not the team climbed
        self.pickupGears = 0
        self.pickupBalls = 0
        self.capacity = 0
        self.AptGears = 0
        self.MissHighGoal = 0 #attempts
        self.prevnotes = '' #simply notes
        self.posfin = 1 #numerical representation of tog
        self.tog = 'boiler' #where the drive team is in accordance to the boiler
        self.togcolor = [(117/255), (117/255), (117/255)]
        #auton
        self.aHighgoal = 0
        self.aLowgoal = 0
        self.aGears = 0
        self.aCrossed = 0 #crossed the base line
        self.color = True #True if blue, False if red

    def getAttr(self): #used in saving and uploading, dumps all vars
        debug("getAttr()", "header 2")
        debug(vars(self))
        return vars(self)
        debug("getAttr() end", "header 2")

    def putData(self, data): #puts the data from the local database into the object
        debug("putData()", "header")
        debug(data)
        data = list(data)
        for i in range(len(data)):
            if data[i] == None: #shouldn't need to be done, but fixing up sqlite3 NULL so that its zero
                debug("Sql nonetype failsafe is being run, this might be a problem")
                data[i] = 0
        debug(str(len(data)))
        try: #getting all of the data out of the fetchone statement earlier
            #next 3 lines are compressed to save space and for no other reason, it is safe to replace the semicolons with newlines
            self.event=data[3]; self.gears=data[4]; self.highgoal=data[5]; self.lowgoal=data[6]; self.climb=data[14]; self.capacity=data[7]; self.pickupBalls=data[8]; self.pickupGears=data[9]
            self.aLowgoal=data[11]; self.aHighgoal=data[10]; self.aGears=data[12]; self.aCrossed=data[13]; self.color=data[15]; debug('ooOOOooOOO working'); self.AptGears=data[16]; self.MissHighGoal=data[17]
            self.prevnotes=data[18]; self.posfin=data[19]
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
            debug("data is lame-o (there is none of it)")
        try:
            self.capacity=data[1]; self.pickupBalls=data[2]; self.pickupGears=data[3]; debug(data[1])
        except:
            debug('ok')
        debug("putCData() end", "header")

#main class, overwrites stacklayout layout from kivy
class Screen(StackLayout):
    prev = ''
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.lastLowVal = 0
        self.choose()

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
                                                        `AptGears` INTEGER,
                                                        `MissHighGoal` INTEGER,
                                                        `notes` TEXT,
                                                        `position` INTEGER,
                                                        PRIMARY KEY(`team`,`round`))''')
        db.execute("CREATE TABLE IF NOT EXISTS `lastscouter` (`name` TEXT)")
        db.execute('''CREATE TABLE IF NOT EXISTS `team`(
                                                        `team`INTEGER NOT NULL,
                                                        `capacity` INTEGER,
                                                        `pickupBalls` INTEGER,
                                                        `pickupGears` INTEGER,
                                                        PRIMARY KEY(`team`))''')
        db.execute("CREATE TABLE IF NOT EXISTS `events` (`currentEvent`)")
        debug("makeDB() end", "header")

    def getlastscouter(self, default=''): #returns last scouter it remembers
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
            return row[0]
        debug("getLastScouter() end", "header")

    def setlastscouter(self, name): #puts last scouter into memory
        debug("setlastscouter()", "header")
        debug(name)
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
        self.name = TextInput(multiline=False, size_hint=(.5, .25), text=self.getlastscouter()) #pulls from database
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
        self.setlastscouter(self.name.text)
        debug("pressGo() end", "title")

    def setTeam(self, team, round, name): #gets the team name from the shared database in the raspberry pi
        debug("setTeam()", "title")
        #unpack info sent by pressGo method
        self.team = Team(team)
        self.team.round = round #it renamed a method but it still works don't question it
        self.team.scouterName = name

        dbl = sqlite3.connect("rounddat.db") #connect to local database
        cl = dbl.cursor()

        cl.execute("CREATE TABLE IF NOT EXISTS `currentEvent` (`events` INTEGER)")
        try:
            db = mysql.connector.connect(host="10.111.49.41", user="pi", passwd="pi", db="matchdat") #connect to pi database
            dbtype = "mysql"
        except:
            db = sqlite3.connect('rounddat.db')
            dbtype = "sqlite"

        debug("db is a %s connection" % dbtype)
        c = db.cursor()
        c.execute("SELECT `currentEvent` FROM `events`")
        self.team.event = c.fetchone()[0]
        debug(self.team.event)
        if dbtype == "mysql":
            debug("putting events into local DB")
            cl.execute("INSERT INTO `events`(`currentEvent`) VALUES (?)", (self.team.event,))
        self.team.prevnotes = "" #reinitialize notes??? may need to be removed

        cl.execute("SELECT * FROM `team` WHERE `team`=?", (team,))
        found = cl.fetchone() #returns None if there is no data
        if not found:
            dbl.execute("INSERT INTO `team`(`team`) VALUES (?);", (team,))
            dbl.commit()
        else:
            self.team.putCData(cl)

        try: #little bit more complex, has to remake the database if not found
            cl.execute("SELECT * FROM `main` WHERE `round`=? AND `team`=?", (round, team)) #this will error if the main table isnt there
            found = cl.fetchone()

        except:
            debug("had to remake db")
            self.makeDB()
            found = False
            pass
        if not found:
            debug("putting data into main...")
            dbl.execute("INSERT INTO `main`(`round`,`team`,`scouterName`,`event`) VALUES (?,?,?,?);", (round, team, name, self.team.event))
            debug("round: %s, team: %s, scouter: %s, event: %s", (round, team, name, self.team.event))
            dbl.execute("UPDATE `main` SET `scouterName`=? WHERE `round`=? AND `team`=? AND `event`=?", (name, round, team, self.team.event))
            dbl.commit()
        else:
            self.team.putData(found)
        debug(self.team.color)

        #grabbing team's color and making the color correct
        if self.team.color == None: #default
            self.team.color = True
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
            self.team.tog = 'boiler'
            self.team.togcolor = [(117/255), (117/255), (117/255)]
        elif self.team.posfin == 2:
            self.team.tog = 'middle'
            self.team.togcolor = [0, (255/255), (42/255)]
        else:
            self.team.tog = 'far'
            self.team.togcolor = [(235/255), (61/255), (255/255)]
        debug("pos color", "header 2")
        debug(self.team.posfin)

        debug(self.team.color)
        c.close()
        cl.close()
        db.close()
        dbl.close()
        debug("setTeam() end", "title")
        self.scrMain()

    #the following functions are called by the buttons on the interface when pressed
    def addLow(self, count, widg): #add to low goals scored
        debug("addLow()")
        self.reloadList = [widg]
        self.team.lowgoal += count
        if self.team.lowgoal <= 0:
            self.team.lowgoal = 0
        widg.text = str(self.team.lowgoal)
    def addHigh(self, count, widg): #add to high goals scored
        debug("addHigh()")
        self.reloadList = [widg]
        self.team.highgoal += count
        if self.team.highgoal <= 0:
            self.team.highgoal = 0
        widg.text = str(self.team.highgoal)
    def addMissHigh(self, count, widg): #add to missed high goals
        debug("addMissHigh()")
        self.reloadList = [widg]
        self.team.MissHighGoal += count
        if self.team.MissHighGoal <= 0:
            self.team.MissHighGoal = 0
        widg.text = str(self.team.MissHighGoal)
    def addGear(self, count, widg): #add to gears scored
        debug("addGear()")
        self.reloadList = [widg]
        self.team.gears += count
        if self.team.gears <= 0:
            self.team.gears = 0
        widg.text = str(self.team.gears)
    def addAptGear(self, count, widg): #add to attempted gears
        debug("addAptGear")
        self.reloadList = [widg]
        self.team.AptGears += count
        if self.team.AptGears <= 0:
            self.team.AptGears = 0
        widg.text = str(self.team.AptGears)
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
    def climbed(self, widg, obj=None): #toggle whether or not the team climbed
        debug("climbed()")
        self.reloadList = [widg]
        self.team.climb = int(not self.team.climb)
        widg.text = "yes" if self.team.climb else "no"
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
    def aAddGear(self, widg, obj=None): #toggle if team used gear in auton
        debug("aAddGear")
        self.reloadList = [widg]
        self.team.aGears = int(not self.team.aGears)
        widg.text = "The team %s use their gear."%("DID"if self.team.aGears else"DIDN'T")
    def aToggleCross(self, widg, obj=None): #toggle if team crossed base line in auton
        debug("aToggleCross")
        self.reloadList = [widg]
        self.team.aCrossed = int(not self.team.aCrossed)
        widg.text = "The team %s cross the ready line."%("DID"if self.team.aCrossed else"DIDN'T")
    def checkpos(self, widg): #toggle team's position
        debug("checkpos")
        self.reloadList = [widg]
        self.team.posfin = self.team.posfin + 1
        debug(self.team.posfin)
        if self.team.posfin >= 3:
            self.team.posfin = self.team.posfin - 3
        if self.team.posfin == 1:
            self.team.tog = 'Boiler'
            self.team.togcolor = [(117/255), (117/255), (117/255)]
        elif self.team.posfin == 2:
            self.team.tog = 'Middle'
            self.team.togcolor = [0, (255/255), (42/255)]
        else:
            self.team.tog = 'Far'
            self.team.togcolor = [(235/255), (61/255), (255/255)]
        self.scrMain()

    #main functions (displays)
    def scrMain(self, obj=None, reload=False): #teleop scr
        debug("scrMain()", "title")
        displist = list()
        self.camefrom = "tele" #used to route the cancel button on the areyousure scr
        #reset menu button text
        self.didSave = "Save"
        self.didUpload = "               Upload \n (Save before uploading)"
        self.didUploadAll = "Upload all"

            #line 1
        lowLbl =       largeSideLabel("Low goal", rgb=[(14/255),(201/255),(170/255)]); displist.append(lowLbl)
        dummyLbl =     cLabel(text="Event " + str(self.team.event), rgb=[0, 0, 0, 1], size_hint=(.23, .075)); displist.append(dummyLbl)
        teamDisp =     largeLabel("Team " + str(self.team.number), rgb=[0, 0, 0, 1]); displist.append(teamDisp)
        dummyLbl2 =    cLabel(text="Scouter " + str(self.team.scouterName), rgb=[0, 0, 0, 1], size_hint=(.23, .075)); displist.append(dummyLbl2)
        highLbl =      largeSideLabel("High goal\n\nHit     Miss", rgb=[(28/255),(201/255),(40/255)]); displist.append(highLbl) #cheesing so that we don't have to make two labels

            #line 2
        lowDisp =      largeSideLabel(str(self.team.lowgoal), rgb=[(14/255),(201/255),(170/255)]); displist.append(lowDisp)
        checkColor =  smallButton("Team Blue" if self.team.color else "Team Red", rgb=self.buttoncolor); checkColor.bind(on_release=lambda x: self.color(checkColor)); displist.append(checkColor)
        checkpos = smallButton(self.team.tog, self.team.togcolor); checkpos.bind(on_release=lambda x: self.checkpos(checkpos)); displist.append(checkpos)
        dummyLbl4 =    largeLabel("Teleop", rgb=[0, 0, 0, 1]); displist.append(dummyLbl4)
        toggleExit =   largeButton("Menu", rgb=[(201/255),(170/255),(28/255)]); toggleExit.bind(on_release=self.scrExit); displist.append(toggleExit)
        highDisp =     smallSideLabel(str(self.team.highgoal), rgb=[(28/255),(201/255),(40/255)]); displist.append(highDisp)
        MissHighDisp = smallSideLabel(str(self.team.MissHighGoal), rgb=[(120/255),(201/255),(40/255)]); displist.append(MissHighDisp)

            #line 3
        incLow1 =      smallSideButton("-1", rgb=[(14/255),(201/255),(170/255)]); incLow1.bind(on_release=lambda x: self.addLow(-1, lowDisp)); displist.append(incLow1)
        incLow3 =      smallSideButton("-3", rgb=[(14/255),(201/255),(170/255)]); incLow3.bind(on_release=lambda x: self.addLow(-3, lowDisp)); displist.append(incLow3)
        capLbl =       largeLabel("Capacity", rgb=[(14/255),(201/255),(170/255)]); displist.append(capLbl)
        toggleAuton =  largeButton("Auton", rgb=[(201/255),(170/255),(28/255)]); toggleAuton.bind(on_release=self.scrAuton); displist.append(toggleAuton)
        toggleCapab =  largeButton("Capability", rgb=[(201/255),(170/255),(28/255)]); toggleCapab.bind(on_release=self.scrCapab); displist.append(toggleCapab)
        decHigh =      smallSideButton("-1", rgb=[(28/255),(201/255),(40/255)]); decHigh.bind(on_release=lambda x: self.addHigh(-1, highDisp)); displist.append(decHigh)
        decMissHigh =  smallSideButton("-1", rgb=[(120/255),(201/255),(40/255)]); decMissHigh.bind(on_release=lambda x: self.addMissHigh(-1, MissHighDisp)); displist.append(decMissHigh)

            #line 4
        incLow9 =     smallSideButton("-9", rgb=[(14/255),(201/255),(170/255)]); incLow9.bind(on_release=lambda x: self.addLow(-9, lowDisp)); displist.append(incLow9)
        incLow15 =     smallSideButton("-15", rgb=[(14/255),(201/255),(170/255)]); incLow15.bind(on_release=lambda x: self.addLow(-15, lowDisp)); displist.append(incLow15)
        capDispAdd =   smallButton("+" + str(self.team.capacity), rgb=[(14/255),(201/255),(170/255)]); capDispAdd.bind(on_release=lambda x: self.addLow(self.team.capacity, lowDisp)); displist.append(capDispAdd)
        capDispSub =   smallButton("-" + str(self.team.capacity), rgb=[(14/255),(201/255),(170/255)]); capDispSub.bind(on_release=lambda x: self.addLow(-self.team.capacity, lowDisp)); displist.append(capDispSub)
        toggleTeam =   largeButton("Team", rgb=[(201/255),(170/255),(28/255)]); toggleTeam.bind(on_release=self.areYouSure); displist.append(toggleTeam)
        togglenotes =  largeButton("Notes", rgb=[(201/255),(170/255),(28/255)]); togglenotes.bind(on_release=self.scrnotes); displist.append(togglenotes)
        addHigh1 =     smallSideButton("-3", rgb=[(28/255),(201/255),(40/255)]); addHigh1.bind(on_release=lambda x: self.addHigh(-3, highDisp)); displist.append(addHigh1)
        addMissHigh1 = smallSideButton("-3", rgb=[(120/255),(201/255),(40/255)]); addMissHigh1.bind(on_release=lambda x: self.addMissHigh(-3, MissHighDisp)); displist.append(addMissHigh1)

            #line 5
        decLow1 =      smallSideButton("1", rgb=[(14/255),(201/255),(170/255)]); decLow1.bind(on_release=lambda x: self.addLow(1, lowDisp)); displist.append(decLow1)
        decLow5 =      smallSideButton("3", rgb=[(14/255),(201/255),(170/255)]); decLow5.bind(on_release=lambda x: self.addLow(5, lowDisp)); displist.append(decLow5)
        climbLbl =     largeLabel("Climbed", rgb=[(201/255),(28/255),(147/255)]); displist.append(climbLbl)
        gearLbl =      smallLabel("Gears", rgb=[(28/255),(129/255),(201/255)]); displist.append(gearLbl)
        gearDisp =     smallLabel(str(self.team.gears), rgb=[(28/255),(129/255),(201/255)]); displist.append(gearDisp)
        AptGearLbl =   smallLabel("AptGears", rgb=[(28/255),0,(201/255)]); displist.append(AptGearLbl)#AptGears is the varible for Miss Gears
        AptGearDisp =  smallLabel(str(self.team.AptGears), rgb=[(28/255),0,(201/255)]); displist.append(AptGearDisp)
        addHigh2 =     smallSideButton("+1", rgb=[(28/255),(201/255),(40/255)]); addHigh2.bind(on_release=lambda x: self.addHigh(1, highDisp)); displist.append(addHigh2)
        addMissHigh2 = smallSideButton("+1", rgb=[(120/255),(201/255),(40/255)]); addMissHigh2.bind(on_release=lambda x: self.addMissHigh(1, MissHighDisp)); displist.append(addMissHigh2)

            #line 6
        decLow10 =     smallSideButton("9", rgb=[(14/255),(201/255),(170/255)]); decLow10.bind(on_release=lambda x: self.addLow(10, lowDisp)); displist.append(decLow10)
        decLow20 =     smallSideButton("15", rgb=[(14/255),(201/255),(170/255)]); decLow20.bind(on_release=lambda x: self.addLow(20, lowDisp)); displist.append(decLow20)
        checkClimb =   largeButton("yes" if self.team.climb else "no", rgb=[(201/255),(28/255),(147/255)]); checkClimb.bind(on_release=lambda x: self.climbed(checkClimb)); displist.append(checkClimb)
        addGear =      smallButton("+", rgb=[(28/255),(129/255),(201/255)]); addGear.bind(on_release=lambda x: self.addGear(1, gearDisp)); displist.append(addGear)
        decGear =      smallButton("-", rgb=[(28/255),(129/255),(201/255)]); decGear.bind(on_release=lambda x: self.addGear(-1, gearDisp)); displist.append(decGear)
        addAptGear =   smallButton("+", rgb=[(28/255),0,(201/255)]); addAptGear.bind(on_release=lambda x: self.addAptGear(1, AptGearDisp)); displist.append(addAptGear)
        decAptGear =   smallButton("-", rgb=[(28/255),0,(201/255)]); decAptGear.bind(on_release=lambda x: self.addAptGear(-1, AptGearDisp)); displist.append(decAptGear)
        addHigh3 =     smallSideButton("+3", rgb=[(28/255),(201/255),(40/255)]); addHigh3.bind(on_release=lambda x: self.addHigh(3, highDisp)); displist.append(addHigh3)
        addMissHigh3 = smallSideButton("+3", rgb=[(120/255),(201/255),(40/255)]); addMissHigh3.bind(on_release=lambda x: self.addMissHigh(3, MissHighDisp)); displist.append(addMissHigh3)

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
        cancel = cButton(text="Cancel", size_hint=(1, .1)); cancel.bind(on_release=self.scrMain if self.camefrom == "tele" else self.scrAuton); displist.append(cancel)
        #row 2
        notes = TextInput(text=str(self.team.prevnotes), multiline=True, size_hint=(1, .8)); notes.bind(on_text_validate=lambda x: self.scrnotes); displist.append(notes)
        #row 3
        save = cButton(text="Save", size_hint=(1, .1)); save.bind(on_release=lambda x: self.savednotes(notes)); displist.append(save)

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

        self.clear_widgets()
        for widg in displist:
            self.add_widget(widg)
        debug("scrAuton() end", "title")

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
        db.execute("UPDATE `main` SET `highgoal`=?,`lowgoal`=?,`gears`=?,`pickupGears`=?,`pickupBalls`=?,`climbed`=?,`capacity`=?,`aHighgoal`=?,`aLowgoal`=?,`aGears`=?,`scouterName`=?,`aCrossed`=?, `team color`=?, `AptGears`=?, `MissHighGoal`=?, `notes`=?, `position`=? WHERE `team`=? AND `round`=? AND `event`=?;",
                   (d["highgoal"],d["lowgoal"],d["gears"],d["pickupGears"],d["pickupBalls"],d["climb"],d["capacity"],d["aHighgoal"],d["aLowgoal"],d["aGears"],d["scouterName"],d["aCrossed"],d["color"],d["AptGears"],d["MissHighGoal"],d["prevnotes"],d["posfin"],d["number"],d["round"],d["event"])
                   ) #sql wizardry, simply takes out all of the stuff stored in d (data) and puts it in its respective places
        db.execute("UPDATE `team` SET `capacity`=?,`pickupGears`=?,`pickupBalls`=? WHERE `team`=?",
                   (d["capacity"],d["pickupGears"],d["pickupBalls"], self.team.number)) #updating the constants storage table
        c = db.cursor()
        c.execute("SELECT * FROM `main` WHERE `round`=? AND `team`=? AND `event`=?", (self.team.round, self.team.number, self.team.event)) #just to check
        debug(c.fetchone())
        db.commit()
        db.close()
        self.didSave = "Saved." #switch button text
        debug("save() end", "title")
        self.scrExit()

    def uploadAll(self, obj=None): #uploads all data in the local database into the pi database
        debug("uploadAll()", "title")
        try:
            db = mysql.connector.connect(host="10.111.49.41", user="pi", passwd="pi", db="matchdat") #connect to pi
        except:
            debug("unable to connect to database, aborting upload")
            self.didAupload = "Failed to connect to the database"
            self.scrExit()
            return
        dbl = sqlite3.connect("rounddat.db")
        cl = dbl.cursor()
        cl.execute("SELECT team, round, scouterName FROM `main`")
        for fetchone in cl.fetchall():
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
        db = mysql.connector.connect(host="10.111.49.41", user="pi", passwd="pi", db="matchdat")
        c = db.cursor()
        dbl = sqlite3.connect("rounddat.db")
        cl = dbl.cursor()
        c.execute("SELECT scouterName, gears, highgoal, lowgoal, capacity, pickupBalls, pickupGears, aHighgoal, aLowgoal, aGears, aCrossed, climbed, `team color`, AptGears, MissHighGoal, notes, position, team, round, event FROM `main` WHERE `round`=? AND `team`=? AND `event`=?", (self.team.round, self.team.number, self.team.event))
        data = c.fetchone()

    def upload(self, obj=None): #uploads loaded data into the pi database
        debug("upload()", "title")
        try:
            db = mysql.connector.connect(host="10.111.49.41", user="pi", passwd="pi", db="matchdat") #connect to pi
        except:
            debug("unable to connect to database, aborting upload")
            self.didUpload = "Failed to connect to the database"
            self.scrExit()
            return
        c = db.cursor(buffered=True)
        self.compatTableau(c)
        dbl = sqlite3.connect("rounddat.db") #connect to local db
        cl = dbl.cursor()
        cl.execute("SELECT * FROM `main`")
        fetchall = cl.fetchall()
        fetchone = None
        for tup in fetchall: #workaround for a bug i was getting on the commented line below
            debug("Target round: %s, number: %s, event: %s" % (self.team.round, self.team.number, self.team.event))
            debug("Actual round: %s, number: %s, event: %s" % (tup[0], tup[1], tup[3]))
            if tup[0] == self.team.round and tup[1] == self.team.number and tup[3] == self.team.event:
                debug("whoag they match, breaking")
                fetchone = tup
                break
        cl.execute("SELECT scouterName, gears, highgoal, lowgoal, capacity, pickupBalls, pickupGears, aHighgoal, aLowgoal, aGears, aCrossed, climbed, `team color`, AptGears, MissHighGoal, notes, position, team, round, event FROM `main` WHERE `round`=? AND `team`=? AND `event`=?", (self.team.round, self.team.number, self.team.event))
        if not fetchone:
            fetchone = cl.fetchone()
        debug(fetchone)
        fetchoneList = list(fetchone) #IF THIS ERRORS THE PROGRAM COULD NOT FIND THE CORRECT DATA TO UPLOAD
        debug("fetchoneList: "+str(fetchoneList))

        c.execute("SELECT * FROM `main` WHERE `team`=%s AND `round`=%s AND `event`=%s", (self.team.number, self.team.round, self.team.event))
        test = c.fetchone()
        if not test: #setting up pi database to take the data
            c.execute("INSERT INTO `main`(`team`,`round`,`event`) VALUES (%s,%s,%s);", (self.team.number, self.team.round, self.team.event))
        elif test: #if the pi database is already set to take the data
            debug("THERE SHOULD BE DATA HERE: " + str(test))

        c.execute("UPDATE `main` SET `scouterName`=%s,`gears`=%s,`highgoal`=%s,`lowgoal`=%s,`capacity`=%s,`pickupBalls`=%s,`pickupGears`=%s,`aHighgoal`=%s,`aLowgoal`=%s,`aGears`=%s,`aCrossed`=%s,`climbed`=%s, `team color`=%s, `AptGears`=%s, `MissHighGoal`=%s, `notes`=%s, `position`=%s WHERE `team`=%s AND `round`=%s AND `event`=%s;",
                  fetchoneList
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

    def compatTableau(self, c):
        debug("compatTableau", "title")
        c.execute("""CREATE TABLE IF NOT EXISTS `tableau` (
                     `team` INTEGER,
                     `round` INTEGER,
                     `event` TEXT,
                     `scouter` TEXT,
                     `phase` TEXT,
                     `action` TEXT,
                     `successes` INTEGER,
                     `misses` INTEGER,
                     `accuracy` INTEGER,
                     `score` INTEGER
                     )""")
        debug(self.team.event)
        d = self.team.getAttr()
        try: accuracy = int((d["highgoal"]/(d["highgoal"]+d["MissHighGoal"]))*100)
        except ZeroDivisionError: accuracy = 0
        c.execute("INSERT INTO tableau (team, round, event, phase, action, successes, misses, accuracy, score) VALUES (" + "%s,"*9 + ");",\
                  (d["number"], d["round"], d["event"], "teleop", "highgoal", d["highgoal"], d["MissHighGoal"], accuracy, int(d["highgoal"]/3))
                  )
        c.execute("INSERT INTO tableau (team, round, event, phase, action, successes, misses, accuracy, score) VALUES (" + "%s,"*9 + ");",
                  (d["number"], d["round"], d["event"], "teleop", "lowgoal", d["lowgoal"], 0, 100, int(d["lowgoal"]/9))
                  )
        misses = d["AptGears"] - d["gears"]
        try: accuracy = int((d["gears"]/(d["gears"]+d["AptGears"]))*100)
        except ZeroDivisionError: accuracy = 0
        c.execute("INSERT INTO tableau (team, round, event, phase, action, successes, misses, accuracy, score) VALUES (" + "%s,"*9 + ");",
                  (d["number"], d["round"], d["event"], "teleop", "gears", d["gears"], misses, accuracy, int(d["gears"]))
                  )
        #you are like a little baby
        #watch this
        succ = 1 if d["climb"] else 0
        miss = 0 if d["climb"] else 1
        c.execute("INSERT INTO tableau (team, round, event, phase, action, successes, misses, accuracy, score) VALUES (" + "%s,"*9 + ");",
                  (d["number"], d["round"], d["event"], "teleop", "climbed", succ, miss, d["climb"], d["climb"]*50)
                  )


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
#        if os.geteuid() != 0:
#            os.system("sudo main.py")
        return Screen()

if __name__ == "__main__":
    MyApp().run()

#wha-pang
