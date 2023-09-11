import PyPDF2
import re
import time
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.clock import Clock

marks = 30


def getChoices(page, fileName):
    if int(fileName.split("_")[1][1:]) < 17:
        myList = [i for i in re.split(r" +|\n+", page) if i.isalpha()][-30:]
        for i in range(len(myList) // 2):
            myList += myList.pop(i + 1)
    else:
        myList = [i for i in re.split(r" +|\n+", page) if i.isalpha()][-28:]
        temp = PyPDF2.PdfFileReader(fileName).getPage(2).extractText()
        myList += [i for i in re.split(r" +|\n+", temp) if i.isalpha()][-12:]
    return myList


class OpenFiles(Screen):
    answers = []

    def file_fire_select(self, fileName):
        try:
            with open(fileName[0], "rb") as f:
                page = PyPDF2.PdfFileReader(f).getPage(1).extractText()
                f.close()
                print(page)
                OpenFiles.answers = getChoices(page, fileName[0])
                init()
                self.manager.current = 'choices'
        except:
            pass


def init():
    Choices.timer = time.perf_counter()
    Choices.start = time.perf_counter()


class Choices(Screen):
    choices = []
    count = 1
    number = StringProperty("1")
    my_clock = StringProperty("00:00")
    timer = 0
    start = 0

    def __init__(self, **kw):
        super().__init__(**kw)
        self.clock()

    def changeTime(self, *args):
        self.my_clock = time.strftime("%M:%S", time.gmtime(time.perf_counter() - self.start))

    def clock(self):
        Clock.schedule_interval(self.changeTime, 1)

    def choose(self, choice):
        self.timer = time.perf_counter() - self.timer
        if self.count < marks:
            Choices.choices.append([choice, self.timer])
            Choices.count += 1
            self.number = str(Choices.count)
        else:
            Choices.choices.append([choice, self.timer])
            self.manager.current = 'recap'
        self.timer = time.perf_counter()


class Recap(Screen):
    result = StringProperty("")

    def getResult(self):
        print(Choices.choices)
        self.result = f"You got {len([i for i in range(len(OpenFiles.answers)) if OpenFiles.answers[i] == Choices.choices[i][0]])}/{Choices.count}"


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file('mcq.kv')


class Mcq(App):
    def build(self):
        return kv


if __name__ == '__main__':
    Mcq().run()
