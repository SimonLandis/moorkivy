from kivy.garden.mapview import MapView
from kivy.clock import Clock
from kivy.app import App
from bikelockmarker import BikeLockMarker, UserMarker
import math


class BikeLockMapView(MapView):
    finding_locks_timer = None
    bike_lock_types = []

    def find_bike_locks_in_view(self):
        try:
            self.finding_locks_timer.cancel()
        except:
            pass
        self.finding_locks_timer = Clock.schedule_once(self.find_bike_locks_in_view, 10)

    def find_bike_locks_in_view(self, *args):
        app = App.get_running_app()
        sql_statement = "SELECT * FROM moordemo;"
        app.cursor.execute(sql_statement)
        bikelocks = app.cursor.fetchall()
        print(bikelocks)
        for bikelock in bikelocks:
            kind = bikelock[1]
            if kind in self.bike_lock_types:
                continue
            else:
                self.distance(bikelock)

    def distance(self, bikelock):
        lat1, lon1 = float(bikelock[2]), float(bikelock[3])
        lat2, lon2 = 39.9526, -75.1652
        radius = 3959 # km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radius * c
        capacity = float(bikelock[1])
        shape = str(bikelock[0])

        if d <= 0.0189394: #looks for locks within 100 feet
            self.add_bike_lock(lat1, lon1) 
            self.add_user_marker(lat2, lon2)
            print(d * 5280)
        elif d <= 0.0473485: #looks for locks within 250 feet
            self.add_bike_lock(lat1, lon1)
            self.add_user_marker(lat2, lon2)
            print(d * 5280)

    def add_bike_lock(self, lat1, lon1): # this adds markers to the map where bike locks are
        lon, lat = lon1, lat1
        marker = BikeLockMarker(lat=lat, lon=lon)
        self.add_widget(marker)

    def add_user_marker(self, lat2, lon2): # adds a marker to show where the user is/default lat lon setting
        lon, lat = lon2, lat2
        marker = UserMarker(lat=lat, lon=lon)
        self.add_widget(marker)