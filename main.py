from kivy.app import App
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import *
from kivy.lang import Builder

import sqlite3

Builder.load_string("""
<cLabel>:
    canvas.before:
        Color:
            rgb: self.rgb
        Rectangle:
            pos: self.pos
            size: self.size

<cButton>:
    background_normal: ""
    background_color: self.rgb
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
def smallLabel(txt, rgb=[.5,.5,.5], height=.075):
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

    def getAttr(self):
        return vars(self)

    def putData(self, c):
        c.execute("SELECT * FROM `main` WHERE `team` = ? AND `round` = ?", (self.number, self.round))
        data = c.fetchone()
        self.gears=data[2]; self.highgoal=data[3]; self.lowgoal=data[4]; self.climb=data[5]; self.capacity=data[6]; self.pickupBalls=data[7]; self.pickupGears=data[8]

class Screen(StackLayout):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.lastLowVal = 0
        self.choose()

    def choose(self):
        self.clear_widgets()
        self.teamsel =  TextInput(multiline=False, size_hint=(.5, (1/3)))
        self.roundsel = TextInput(multiline=False, size_hint=(.5, (1/3)))
        gobutton = cButton(text="Go", size_hint=(1, (1/3)))
        gobutton.bind(on_release=self.pressGo)
        self.add_widget(cLabel(rgb=[(14/255),(201/255),(170/255)], text="Enter team name:", size_hint=(.5, (1/3))))
        self.add_widget(self.teamsel)
        self.add_widget(cLabel(rgb=[(14/255),(201/255),(170/255)], text="Enter round number:", size_hint=(.5, (1/3))))
        self.add_widget(self.roundsel)
        self.add_widget(gobutton)

    def pressGo(self, obj):
        if self.teamsel.text and self.roundsel.text:
            self.setTeam(self.teamsel.text, self.roundsel.text)
        else:
            print("unable to setTeam, number %s, round %s" % (self.teamsel.text, self.roundsel.text))
            self.choose()

    def setTeam(self, team, round):
        self.team = Team(team)
        self.team.round = round
        db = sqlite3.connect("test")
        c = db.cursor()
        c.execute("SELECT * from `main` where round = ? and team = ?", (round, team))
        if not c.fetchone():
            db.execute("INSERT INTO `main`(`round`,`team`) VALUES (?,?);", (round, team))
            db.commit()
        else:
            self.team.putData(c)
        #TODO add else statement that puts stored data from database into the self.team
        c.close()
        db.close()
        self.scrMain()

    #the following functions are called by the buttons on the interface when pressed
    def addLow(self, count):
        self.team.lowgoal += count
        self.scrMain()
    def addHigh(self, count):
        self.team.highgoal += count
        self.scrMain()
    def addGear(self, count):
        self.team.gears += count
        self.scrMain()
    def canPickGear(self, obj=None):
        if not self.team.pickupGears: self.team.pickupGears = True
        else:                         self.team.pickupGears = False
        self.scrCapab()
    def canPickBall(self, obj=None):
        if not self.team.pickupBalls: self.team.pickupBalls = True
        else:                         self.team.pickupBalls = False
        self.scrCapab()
    def climbed(self, obj=None):
        if self.team.climb == False: self.team.climb = True
        else:                        self.team.climb = False
        self.scrMain()

    #main functions (displays)
    def scrMain(self, obj=None):
        self.clear_widgets()
        displist = list()
        #lsl - 15.5, ll - 23, ssl - 7.75, sl - 11.5
        #sea foam green: , rgb=[(14/255),(201/255),(170/255)] : low goal
        #dark magenta:   , rgb=[(201/255),(28/255),(147/255)] : climbed
        #fair blue:      , rgb=[(28/255),(129/255),(201/255)] : gears
        #happy green:    , rgb=[(28/255),(201/255),(40/255)] :  high goal
        #fair orange:    , rgb=[(201/255),(170/255),(28/255)] : switch

            #line 1
        lowLbl =       largeSideLabel("Low goal", rgb=[(14/255),(201/255),(170/255)]); displist.append(lowLbl)
        dummyLbl =     cLabel(text=" ", size_hint=(.23, .075)); displist.append(dummyLbl)
        teamDisp =     largeLabel(str(self.team.number)); displist.append(teamDisp)
        dummyLbl2 =    cLabel(text=" ", size_hint=(.23, .075)); displist.append(dummyLbl2)
        highLbl =      largeSideLabel("High goal", rgb=[(28/255),(201/255),(40/255)]); displist.append(highLbl)

            #line 2
        lowDisp =      largeSideLabel(str(self.team.lowgoal), rgb=[(14/255),(201/255),(170/255)]); displist.append(lowDisp)
        dummyLbl4 =    cLabel(text=" ", size_hint=(.69, .075)); displist.append(dummyLbl4)
        highDisp =     largeSideLabel(str(self.team.highgoal), rgb=[(28/255),(201/255),(40/255)]); displist.append(highDisp)

            #line 3
        incLow1 =      smallSideButton("1", rgb=[(14/255),(201/255),(170/255)]); incLow1.bind(on_release=lambda x: self.addLow(1)); displist.append(incLow1)
        incLow5 =      smallSideButton("5", rgb=[(14/255),(201/255),(170/255)]); incLow5.bind(on_release=lambda x: self.addLow(5)); displist.append(incLow5)
        capLbl =       largeLabel("Capacity", rgb=[(14/255),(201/255),(170/255)]); displist.append(capLbl)
        toggleAuton =  largeButton("Auton", rgb=[(201/255),(170/255),(28/255)]); displist.append(toggleAuton)# toggleAuton.bind(on_release=self.scrAuton); displist.append(toggleAuton) #TODO - add auton screen
        toggleCapab =  largeButton("Capability", rgb=[(201/255),(170/255),(28/255)]); toggleCapab.bind(on_release=self.scrCapab); displist.append(toggleCapab)
        decHigh =      largeSideButton("-1", rgb=[(28/255),(201/255),(40/255)]); decHigh.bind(on_release=lambda x: self.addHigh(-1)); displist.append(decHigh)

            #line 4
        incLow10 =     smallSideButton("10", rgb=[(14/255),(201/255),(170/255)]); incLow10.bind(on_release=lambda x: self.addLow(10)); displist.append(incLow10)
        incLow20 =     smallSideButton("20", rgb=[(14/255),(201/255),(170/255)]); incLow20.bind(on_release=lambda x: self.addLow(20)); displist.append(incLow20)
        capDispAdd =   smallButton("+" + str(self.team.capacity), rgb=[(14/255),(201/255),(170/255)]); capDispAdd.bind(on_release=lambda x: self.addLow(self.team.capacity)); displist.append(capDispAdd)
        capDispSub =   smallButton("-" + str(self.team.capacity), rgb=[(14/255),(201/255),(170/255)]); capDispSub.bind(on_release=lambda x: self.addLow(-self.team.capacity)); displist.append(capDispSub)
        toggleTeam =   largeButton("Team", rgb=[(201/255),(170/255),(28/255)]); toggleTeam.bind(on_release=lambda x: self.choose()); displist.append(toggleTeam)
        toggleExit =   largeButton("Exit", rgb=[(201/255),(170/255),(28/255)]); toggleExit.bind(on_release=self.scrExit); displist.append(toggleExit)
        addHigh1 =     largeSideButton("-3", rgb=[(28/255),(201/255),(40/255)]); addHigh1.bind(on_release=lambda x: self.addHigh(-3)); displist.append(addHigh1)

            #line 5
        decLow1 =      smallSideButton("-1", rgb=[(14/255),(201/255),(170/255)]); decLow1.bind(on_release=lambda x: self.addLow(-1)); displist.append(decLow1)
        decLow5 =      smallSideButton("-5", rgb=[(14/255),(201/255),(170/255)]); decLow5.bind(on_release=lambda x: self.addLow(-5)); displist.append(decLow5)
        climbLbl =     largeLabel("Climbed", rgb=[(201/255),(28/255),(147/255)]); displist.append(climbLbl)
        gearLbl =      largeLabel("Gears", rgb=[(28/255),(129/255),(201/255)]); displist.append(gearLbl)
        gearDisp =     largeLabel(str(self.team.gears), rgb=[(28/255),(129/255),(201/255)]); displist.append(gearDisp)
        addHigh2 =     largeSideButton("+1", rgb=[(28/255),(201/255),(40/255)]); addHigh2.bind(on_release=lambda x: self.addHigh(1)); displist.append(addHigh2)

            #line 6
        decLow10 =     smallSideButton("-10", rgb=[(14/255),(201/255),(170/255)]); decLow10.bind(on_release=lambda x: self.addLow(-10)); displist.append(decLow10)
        decLow20 =     smallSideButton("-20", rgb=[(14/255),(201/255),(170/255)]); decLow20.bind(on_release=lambda x: self.addLow(-20)); displist.append(decLow20)
        checkClimb =   largeButton("yes" if self.team.climb else "no", rgb=[(201/255),(28/255),(147/255)]); checkClimb.bind(on_release=lambda x: self.climbed()); displist.append(checkClimb)
        addGear =      largeButton("+", rgb=[(28/255),(129/255),(201/255)]); addGear.bind(on_release=lambda x: self.addGear(1)); displist.append(addGear)
        decGear =      largeButton("-", rgb=[(28/255),(129/255),(201/255)]); decGear.bind(on_release=lambda x: self.addGear(-1)); displist.append(decGear)
        addHigh3 =     largeSideButton("+3", rgb=[(28/255),(201/255),(40/255)]); addHigh3.bind(on_release=lambda x: self.addHigh(3)); displist.append(addHigh3)

        for widg in displist:
            self.add_widget(widg)

    def scrExit(self, obj=None):
        self.clear_widgets()
        displist = list()

        cancel =   Button(text="Cancel", size_hint=(1,.1)); cancel.bind(on_release=self.scrMain); displist.append(cancel)
        saveExit = Button(text="Save and exit", size_hint=(1,.8)); saveExit.bind(on_release=self.saveAndExit); displist.append(saveExit)
        exit =     Button(text="Exit", size_hint=(1, .1)); exit.bind(on_release=self.areYouSure); displist.append(exit)

        for i in displist:
            self.add_widget(i)

    def scrCapab(self, obj=None, cap=None):
        self.clear_widgets()
        displist = list()
        if not cap == None:
            self.team.capacity = cap

        cancel = Button(text="Cancel", size_hint=(1, .1)); cancel.bind(on_release=self.scrMain); displist.append(cancel)
        PGMessage = "The robot %s pickup gears off of the ground." % ("CAN" if self.team.pickupGears else "CAN'T")
        togglePG = Button(text=PGMessage, size_hint=(.5, .45)); togglePG.bind(on_release=self.canPickGear); displist.append(togglePG)
        PBMessage = "The robot %s pickup balls off of the ground." % ("CAN" if self.team.pickupBalls else "CAN'T")
        togglePB = Button(text=PBMessage, size_hint=(.5, .45)); togglePB.bind(on_release=self.canPickBall); displist.append(togglePB)
        capLbl = Label(text="Capacity:\n%s" % self.team.capacity, size_hint=(.5, .45)); displist.append(capLbl)
        capChange = TextInput(multiline=False, size_hint=(.5, .45)); capChange.bind(on_text_validate=lambda x: self.scrCapab(cap=int(capChange.text))); displist.append(capChange)

        for i in displist:
            self.add_widget(i)

    def saveAndExit(self, obj=None):
        db = sqlite3.connect("test")
        d = self.team.getAttr()
        print(d)
        db.execute("UPDATE `main` SET `highgoal`=?,`lowgoal`=?,`gears`=?,`pickupGears`=?,`pickupBalls`=?,`climbed`=?,`capacity`=? WHERE `team`=? AND `round`=?;",
                   (d["highgoal"],d["lowgoal"],d["gears"],d["pickupGears"],d["pickupBalls"],d["climb"],d["capacity"],d["number"],d["round"])
                   )
        db.commit()
        db.close()
        quit()

    def areYouSure(self, obj=None):
        self.clear_widgets()
        displist = list()
        AYSLbl = Label(text="Are you sure?", size_hint=(1,.1)); displist.append(AYSLbl)
        yes = Button(text="Yes", size_hint=(1,.4)); yes.bind(on_release=quit); displist.append(yes)
        no =  Button(text="No", size_hint=(1,.5)); no.bind(on_release=self.scrMain); displist.append(no)

        for i in displist:
            self.add_widget(i)

class myLabel(Widget):
    pass

class MyApp(App):
    def build(self):
        return Screen()

if __name__ == "__main__":
    MyApp().run()
