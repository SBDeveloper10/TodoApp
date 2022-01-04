from kivy.core.text import LabelBase
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder
import datetime
from datetime import date
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.core.window import Window
from kivymd.uix.snackbar import Snackbar

Window.size = (350, 600)


class TodoCard(FakeRectangularElevationBehavior, MDFloatLayout):
    title = StringProperty()
    description = StringProperty()


class ToDoApp(MDApp):

    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("Main.kv"))
        screen_manager.add_widget(Builder.load_file("AddTodo.kv"))
        return screen_manager

    def on_start(self):
        today = date.today()
        wd = date.weekday(today)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().strftime("%b"))
        day = str(datetime.datetime.now().strftime("%d"))
        screen_manager.get_screen("main").date.text = f"{days[wd]}, {day} {month} {year}"
        # print(f"{days[wd]}, {day} {month} {year}")
        # screen_manager.get_screen("main").date.text = f"{day} {month} {year}"
        # screen_manager.get_screen("main").day.text = f"{days[wd]},"

    def on_complete(self, checkbox, value, bar2, description):
        if value:
            description.text = f"[s]{description.text}[/s]"
            bar2.md_bg_color = 0, 179/255, 0, 1
        else:
            remove = ["[s]", "[/s]"]
            for i in remove:
                description.text = description.text.replace(i, "")
            bar2.md_bg_color = 1, 170/255, 23/255, 1

    def add_todo(self, title, description):
        if title != "" and description != "" and len(title) < 21 and len(description) < 61:
            screen_manager.current = "main"
            screen_manager.transition.direction = "right"
            screen_manager.get_screen("main").todo_list.add_widget(TodoCard(title=title, description=description))
            screen_manager.get_screen("add_todo").title.text = ""
            screen_manager.get_screen("add_todo").description.text = ""
        elif title == "":
            Snackbar(text="Title is missing", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()
        elif description == "":
            Snackbar(text="Description is missing", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()
        elif len(title) > 21:
            Snackbar(text="Title length should be < 20!", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10)*2))/Window.width, bg_color=(1, 170/255, 23/255, 1),
                     font_size="18sp").open()
        elif len(description) > 21:
            Snackbar(text="Description length should be < 60!", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10)*2))/Window.width, bg_color=(1, 170/255, 23/255, 1),
                     font_size="18sp").open()


if __name__ == "__main__":
    LabelBase.register(name="Poppins", fn_regular="Your Font Path\\Poppins-Regular.ttf")
    LabelBase.register(name="BPoppins", fn_regular="Your Font Path \\Poppins-SemiBold.ttf")
    ToDoApp().run()
