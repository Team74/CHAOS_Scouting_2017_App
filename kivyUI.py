from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import *
from kivy.lang import Builder

class Team:
    def __init__(self, number):
        self.number = number
        self.chevaldefrise = 0
        self.drawbridge = 0
        self.moat = 0
        self.portcullis = 0
        self.ramparts = 0
        self.rockwall = 0
        self.roughterrain = 0
        self.sallyport = 0


class Screen(GridLayout):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.choose()

    def choose(self):
        self.cols = 2
        self.add_widget(Label(text="Enter team name:"))
        teamsel = TextInput(multiline=False)
        teamsel.bind(on_text_validate=self.setTeam)
        self.add_widget(teamsel)

    def setTeam(self, team):
        self.team = Team(team)
        self.menu()

    def makeImage(self, name, path):
        exec("self.%s = Image(source='%s', allow_stretch=True, keep_ratio=False)" % (name, path))
        exec("exec('%sbtn = Button(text=%s: %s)' % (name, name, self.team.%s))" % name)

    def menu(self, team=None):
        self.cols = 5
        self.clear_widgets()

        self.Moat = Image(source="kivyimage/Moat.png", allow_stretch = True, keep_ratio = False)
        moatbtn = Button(text="Moat: %s" % self.team.moat)
        moatbtn.bind(on_press=self.newscreen)

        self.Portcullis = Image(source="kivyimage/Portcullis.png", allow_stretch=True, keep_ratio = False)
        portbtn = Button(text="Portcullis: %s" % self.team.portcullis)
        portbtn.bind(on_press=self.newscreen)

        self.SallyPort = Image(source="kivyimage/Sally-Port.png", allow_stretch=True, keep_ratio = False)
        sportbtn = Button(text="SallyPort: %s" % self.team.sallyport)
        sportbtn.bind(on_press=self.newscreen)

        self.Ramparts = Image(source="kivyimage/Ramparts.png", allow_stretch=True, keep_ratio = False)
        rampbtn = Button(text="Ramparts: %s" % self.team.ramparts)
        rampbtn.bind(on_press=self.newscreen)

        self.ChevaldeFrise = Image(source="kivyimage/Cheval-de-Frise.png", allow_stretch=True, keep_ratio = False)
        chevbtn = Button(text="ChevaldeFrise: %s" % self.team.chevaldefrise)
        chevbtn.bind(on_press=self.newscreen)

        self.RoughTerrain = Image(source="kivyimage/Rough-Terrain.png", allow_stretch=True, keep_ratio = False)
        roughbtn = Button(text="RoughTerrain: %s" % self.team.roughterrain)
        roughbtn.bind(on_press=self.newscreen)

        self.Drawbridge = Image(source="kivyimage/Drawbridge.png", allow_stretch=True, keep_ratio = False)
        drawbtn = Button(text="Drawbridge: %s" % self.team.drawbridge)
        drawbtn.bind(on_press=self.newscreen)

        self.RockWall = Image(source="kivyimage/Rock-Wall.png", allow_stretch=True, keep_ratio = False)
        rockbtn = Button(text="RockWall: %s" % self.team.rockwall)
        rockbtn.bind(on_press=self.newscreen)

        self.Upper = Image(source="kivyimage/tower.png", allow_stretch=True, keep_ratio=False)
        towerbtnU = Button(text="Upper")
        towerbtnU.bind(on_press=self.newscreen)

        self.Lower = Image(source="kivyimage/tower.png", allow_stretch=True, keep_ratio=False)
        towerbtnD = Button(text="Lower")
        towerbtnD.bind(on_press=self.newscreen)

        self.add_widget(self.Moat)
        self.add_widget(self.Portcullis)
        self.add_widget(self.SallyPort)
        self.add_widget(self.Ramparts)
        self.add_widget(self.Upper)

        self.add_widget(moatbtn)
        self.add_widget(portbtn)
        self.add_widget(sportbtn)
        self.add_widget(rampbtn)
        self.add_widget(towerbtnU)

        self.add_widget(self.ChevaldeFrise)
        self.add_widget(self.RoughTerrain)
        self.add_widget(self.Drawbridge)
        self.add_widget(self.RockWall)
        self.add_widget(self.Lower)

        self.add_widget(chevbtn)
        self.add_widget(roughbtn)
        self.add_widget(drawbtn)
        self.add_widget(rockbtn)
        self.add_widget(towerbtnD)

    def newscreen(self, btn):
        self.clear_widgets()
        self.cols = 1
        if " " in btn.text:
            btn.text = btn.text[:list(btn.text).index(" ")-1]
        exec("self.add_widget(self.%s)" % btn.text)
        print(btn.text.lower())
        exec("self.team.%s += 1" % btn.text.lower())
        exec("print(self.team.%s)" % btn.text.lower())
        backbtn = Button(text="back")
        backbtn.bind(on_press=self.menu)
        self.add_widget(backbtn)

class MyApp(App):
    def build(self):
        return Screen()

if __name__ == "__main__":
    sample = MyApp()
    sample.run()
