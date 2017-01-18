from kivy.app import App
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import *
from kivy.lang import Builder

w = Builder.load_string("""
<Button>:
    canvas:
        Color:
            rgb: (1, 0, 0)
<Label>:
    canvas:
        Color:
            rgb: (0, 1, 0)
""")

#the following functions are for decluttering the scr functions
def smallButton(txt, height=.1666666666666667):
    return Button(text=txt, size_hint=(.115, height))
def smallLabel(txt, height=.075):
    return Label(text=txt, size_hint=(.115, height))

def smallSideButton(txt, height=.1666666666666667):
    return Button(text=txt, size_hint=(.0775, height))
def smallSideLabel(txt, height=.1666666666666667):
    return Label(text=txt, size_hint=(.0775, height))

def largeButton(txt, height=.1666666666666667):
    return Button(text=txt, size_hint=(.23, height))
def largeLabel(txt, height=.1666666666666667):
    return Label(text=txt, size_hint=(.23, height))

def largeSideButton(txt, height=.1666666666666667):
    return Button(text=txt, size_hint=(.155, height))
def largeSideLabel(txt, height=.1666666666666667):
    return Label(text=txt, size_hint=(.155, height))

class Team:
    def __init__(self, number):
        self.number = number
        self.highgoal = 0
        self.lowgoal = 0
        self.gears = 0
        self.pickupGears = False
        self.pickupBalls = False
        self.climb = False
        self.capacity = 0


class Screen(StackLayout):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.lastLowVal = 0
        self.choose()

    def choose(self):
        self.clear_widgets
        teamsel = TextInput(multiline=False, size_hint=(.5, 1))
        teamsel.bind(on_text_validate=lambda x: self.setTeam(teamsel.text))
        print(teamsel.size)
        print(teamsel.size_hint)
        self.add_widget(Label(text="Enter team name:", size_hint=(.5, 1)))
        self.add_widget(teamsel)

    def setTeam(self, team):
        self.team = Team(team)
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
    def canPickGear(self):
        if self.team.pickupGears == False: self.team.pickupGears = True
        else:                              self.team.pickupGears = False
        self.scrMain()
    def climbed(self):
        if self.team.climb == False: self.team.climb = True
        else:                        self.team.climb = False
        self.scrMain()

    #main functions (displays)
    def scrMain(self, team=None): #screen for counting goals and gears
        self.minimum_height = 100
        self.minimum_width = 150
        self.clear_widgets()
        displist = list()
        #lsl - 15.5, ll - 23, ssl - 7.75, sl - 11.5

            #line 1
        lowLbl =       largeSideLabel("Low goal"); displist.append(lowLbl)
        dummyLbl =     Label(text=" ", size_hint=(.23, .075)); displist.append(dummyLbl)
        teamDisp =     largeLabel(str(self.team.number)); displist.append(teamDisp)
        dummyLbl2 =    Label(text=" ", size_hint=(.23, .075)); displist.append(dummyLbl2)
        highLbl =      largeSideLabel("High goal"); displist.append(highLbl)

            #line 2
        lowDisp =      largeSideLabel(str(self.team.lowgoal)); displist.append(lowDisp)
        dummyLbl4 =    Label(text=" ", size_hint=(.69, .075)); displist.append(dummyLbl4)
        highDisp =     largeSideLabel(str(self.team.highgoal)); displist.append(highDisp)

            #line 3
        incLow1 =      smallSideButton("1"); incLow1.bind(on_press=lambda x: self.addLow(1)); displist.append(incLow1)
        incLow5 =      smallSideButton("5"); incLow5.bind(on_press=lambda x: self.addLow(5)); displist.append(incLow5)
        capLbl =       largeLabel("Capacity"); displist.append(capLbl)
        toggleAuton =  largeButton("Auton"); displist.append(toggleAuton)# toggleAuton.bind(on_press=self.scrAuton); displist.append(toggleAuton) #TODO - add auton screen
        toggleCapab =  largeButton("Capability"); displist.append(toggleCapab)# toggleCapab.bind(on_press=self.scrCapab); displist.append(toggleCapab) #TODO - add capability screen
        decHigh =      largeSideButton("-"); decHigh.bind(on_press=lambda x: self.addHigh(-1)); displist.append(decHigh)

            #line 4
        incLow10 =     smallSideButton("10"); incLow10.bind(on_press=lambda x: self.addLow(10)); displist.append(incLow10)
        incLow20 =     smallSideButton("20"); incLow20.bind(on_press=lambda x: self.addLow(20)); displist.append(incLow20)
        capDisp =      largeButton(str(self.team.capacity)); capDisp.bind(on_press=lambda x: self.addLow(self.team.capacity)); displist.append(capDisp)
        toggleTeam =   largeButton("Team"); toggleTeam.bind(on_press=lambda x: self.choose()); displist.append(toggleTeam)
        toggleExit =   largeButton("Exit"); displist.append(toggleExit)# toggleExit.bind(on_press=self.scrExit); displist.append(toggleExit) #TODO - add exit screen (will be able to choose to submit and exit, exit, or go back)
        addHigh1 =     largeSideButton(" "); addHigh1.bind(on_press=lambda x: self.addHigh(1)); displist.append(addHigh1)

            #line 5
        decLow1 =      smallSideButton("-1"); decLow1.bind(on_press=lambda x: self.addLow(-1)); displist.append(decLow1)
        decLow5 =      smallSideButton("-5"); decLow5.bind(on_press=lambda x: self.addLow(-5)); displist.append(decLow5)
        climbLbl =     largeLabel("Climbed"); displist.append(climbLbl)
        gearLbl =      largeLabel("Gears"); displist.append(gearLbl)
        gearDisp =     largeLabel(str(self.team.gears)); displist.append(gearDisp)
        addHigh2 =     largeSideButton("+"); addHigh2.bind(on_press=lambda x: self.addHigh(1)); displist.append(addHigh2)

            #line 6
        decLow10 =     smallSideButton("-10"); decLow10.bind(on_press=lambda x: self.addLow(-10)); displist.append(decLow10)
        decLow20 =     smallSideButton("-20"); decLow20.bind(on_press=lambda x: self.addLow(-20)); displist.append(decLow20)
        checkClimb =   largeButton("yes" if self.team.climb == True else "no"); checkClimb.bind(on_press=lambda x: self.climbed()); displist.append(checkClimb)
        addGear =      largeButton("+"); addGear.bind(on_press=lambda x: self.addGear(1)); displist.append(addGear)
        decGear =      largeButton("-"); decGear.bind(on_press=lambda x: self.addGear(-1)); displist.append(decGear)
        addHigh3 =     largeSideButton(" "); addHigh3.bind(on_press=lambda x: self.addHigh(1)); displist.append(addHigh3)

        for widg in displist:
            self.add_widget(widg)



class MyApp(App):
    def build(self):
        return Screen()

if __name__ == "__main__":
    sample = MyApp()
    sample.run()
