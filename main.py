import requests

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup


# Change this to your online Flask server later.
API_URL = "http://127.0.0.1:8000"


class HomeScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=12
        )

        title = Label(
            text="PIONEER'S FC",
            font_size=32,
            bold=True,
            size_hint_y=None,
            height=70
        )

        slogan = Label(
            text="ONE TEAM • ONE DREAM",
            font_size=18,
            size_hint_y=None,
            height=50
        )

        layout.add_widget(title)
        layout.add_widget(slogan)

        buttons = [
            ("👥 PLAYERS", "players"),
            ("⚽ MATCHES", "matches"),
            ("⭐ MATCH RATINGS", "ratings"),
            ("🗳️ FANS' FAVOURITE", "votes"),
            ("🏆 BEST PLAYER", "votes"),
        ]

        for text, screen in buttons:
            button = Button(
                text=text,
                size_hint_y=None,
                height=60
            )

            button.bind(
                on_press=lambda x, s=screen:
                self.open_screen(s)
            )

            layout.add_widget(button)

        self.add_widget(layout)

    def open_screen(self, screen):
        self.manager.current = screen


class PlayersScreen(Screen):

    def on_enter(self):
        self.load_players()

    def load_players(self):

        self.clear_widgets()

        scroll = ScrollView()

        grid = GridLayout(
            cols=1,
            spacing=10,
            padding=15,
            size_hint_y=None
        )

        grid.bind(minimum_height=grid.setter("height"))

        title = Label(
            text="PIONEER'S FC PLAYERS",
            font_size=25,
            bold=True,
            size_hint_y=None,
            height=60
        )

        grid.add_widget(title)

        try:

            response = requests.get(
                API_URL + "/players",
                timeout=5
            )

            players = response.json()

            if not players:
                grid.add_widget(
                    Label(
                        text="No players added yet.",
                        size_hint_y=None,
                        height=50
                    )
                )

            for player in players:

                text = (
                    f"#{player['number']}  "
                    f"{player['name']}\n"
                    f"{player['position']}"
                )

                card = Button(
                    text=text,
                    size_hint_y=None,
                    height=90
                )

                grid.add_widget(card)

        except Exception as error:

            grid.add_widget(
                Label(
                    text="Unable to connect to server.",
                    size_hint_y=None,
                    height=50
                )
            )

        back = Button(
            text="← BACK",
            size_hint_y=None,
            height=60
        )

        back.bind(
            on_press=lambda x:
            setattr(self.manager, "current", "home")
        )

        grid.add_widget(back)

        scroll.add_widget(grid)

        self.add_widget(scroll)


class MatchesScreen(Screen):

    def on_enter(self):
        self.load_matches()

    def load_matches(self):

        self.clear_widgets()

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10
        )

        title = Label(
            text="MATCHES",
            font_size=28,
            bold=True
        )

        layout.add_widget(title)

        try:

            response = requests.get(
                API_URL + "/matches",
                timeout=5
            )

            matches = response.json()

            if not matches:

                layout.add_widget(
                    Label(
                        text="No matches available."
                    )
                )

            for match in matches:

                layout.add_widget(
                    Label(
                        text=(
                            f"Pioneer's FC vs "
                            f"{match['opponent']}\n"
                            f"{match['date']} • "
                            f"{match['venue']}\n"
                            f"Result: {match['result']}"
                        ),
                        size_hint_y=None,
                        height=100
                    )
                )

        except:

            layout.add_widget(
                Label(
                    text="Unable to connect to server."
                )
            )

        back = Button(
            text="← BACK",
            size_hint_y=None,
            height=60
        )

        back.bind(
            on_press=lambda x:
            setattr(self.manager, "current", "home")
        )

        layout.add_widget(back)

        self.add_widget(layout)


class RatingsScreen(Screen):

    def on_enter(self):

        self.clear_widgets()

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        layout.add_widget(
            Label(
                text="⭐ MATCH RATINGS",
                font_size=28,
                bold=True
            )
        )

        try:

            response = requests.get(
                API_URL + "/ratings",
                timeout=5
            )

            ratings = response.json()

            for player in ratings:

                layout.add_widget(
                    Label(
                        text=(
                            f"{player['name']}  "
                            f"⭐ {player['average_rating']}\n"
                            f"Ratings: {player['votes']}"
                        ),
                        size_hint_y=None,
                        height=70
                    )
                )

        except:

            layout.add_widget(
                Label(
                    text="Unable to connect to server."
                )
            )

        back = Button(
            text="← BACK",
            size_hint_y=None,
            height=60
        )

        back.bind(
            on_press=lambda x:
            setattr(self.manager, "current", "home")
        )

        layout.add_widget(back)

        self.add_widget(layout)


class VotesScreen(Screen):

    def on_enter(self):

        self.clear_widgets()

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        layout.add_widget(
            Label(
                text="🗳️ PLAYER VOTING",
                font_size=28,
                bold=True
            )
        )

        layout.add_widget(
            Label(
                text=(
                    "Fans' Favourite and Best Player\n"
                    "voting will appear here."
                )
            )
        )

        back = Button(
            text="← BACK",
            size_hint_y=None,
            height=60
        )

        back.bind(
            on_press=lambda x:
            setattr(self.manager, "current", "home")
        )

        layout.add_widget(back)

        self.add_widget(layout)


class PioneersFCApp(App):

    def build(self):

        manager = ScreenManager()

        manager.add_widget(
            HomeScreen(name="home")
        )

        manager.add_widget(
            PlayersScreen(name="players")
        )

        manager.add_widget(
            MatchesScreen(name="matches")
        )

        manager.add_widget(
            RatingsScreen(name="ratings")
        )

        manager.add_widget(
            VotesScreen(name="votes")
        )

        return manager


if __name__ == "__main__":
    PioneersFCApp().run()
