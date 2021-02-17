
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from taskss import TaskData


Window.clearcolor = (192/255, 204/255, 209/255, 1)



class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)

                self.reset()

                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class MyRelativeLayout(RelativeLayout):
    pass


class MainWindow(Screen):
    n = ObjectProperty(None)
    current = ""
    label_wid = ObjectProperty(None)

    def logOut(self):
        sm.current = "account"

    def editTasks(self):
        sm.current = "tasks"

    def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        self.n.text = "Hello, " + name + " !"

    def do_action(self, *args):
        #taskname, description, time = td.get_usertasks(self.current)
        self.label_wid.text = 'Task Completed'

class TaskWindow(Screen):
    t = ObjectProperty(None)
    current = ""

    tasknamee = ObjectProperty(None)
    description = ObjectProperty(None)
    time = ObjectProperty(None)

    def mainWin(self):
        sm.current = "main"

    def on_enter(self, *args):
        #password, name, created = db.get_user(self.current)
        self.t.text = "Edit Task Assignments: "
        #self.email.text = " "
        #self.created.text = " "

# inserts task text into usertasks.txt
    def submit(self):
        if self.tasknamee.text != "":
            if self.description.text != "":
                 if self.time != "" and self.time.text.count(":") == 1:
                    td.add_usertasks(self.tasknamee.text, self.description.text, self.time.text)

                    self.reset()

                    sm.current = "tasks"
                 else:
                    invalidTime()
            else:
                invalidForm()

    def login(self):
        self.reset()
        sm.current = "tasks"

    def reset(self):
        self.tasknamee.text = ""
        self.description.text = ""
        self.time.text = ""

class AccountWindow(Screen):
    h = ObjectProperty(None)
    current = ""

    def mainWin(self):
        sm.current = "main"

    def on_enter(self, *args):
        self.h.text = "Account Details "

class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()

def invalidTime():
    pop = Popup(title='Invalid Time',
                  content=Label(text='Please include " : " when inputting time (i.e. 9:00 AM) .'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase("users.txt")

# new
td = TaskData("usertasks.txt")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), MainWindow(name="main"), TaskWindow(name="tasks"), AccountWindow(name="account")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm



if __name__ == "__main__":
    MyMainApp().run()
