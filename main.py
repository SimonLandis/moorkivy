import sqlite3
from kivymd.app import MDApp
from bikelockmapview import BikeLockMapView


class MainApp(MDApp):
    connection = None
    cursor = None

    def on_start(self):
        self.connection = sqlite3.connect("bikelocks.db")
        self.cursor = self.connection.cursor()


MainApp().run()
