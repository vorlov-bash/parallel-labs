import random

from actors.bus import Bus
from actors.bus_stop import BusStop

if __name__ == '__main__':
    bus_stops = [
        BusStop.start('Bus stop #1', max_size=10),
        BusStop.start('Bus stop #2', max_size=5),
        BusStop.start('Bus stop #3', max_size=6),
        BusStop.start('Bus stop #4', max_size=3),
    ]

    buses = [
        Bus.start(3, 'AA4783KB', bus_stops),
        Bus.start(6, 'AA8888KB', bus_stops),
        Bus.start(4, 'AA9999KB', bus_stops),
        Bus.start(2, 'AA9090KB', bus_stops),
    ]
