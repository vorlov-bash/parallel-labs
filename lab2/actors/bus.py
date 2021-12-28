import logging
import random

import pykka
import time
from typing import Optional, TYPE_CHECKING, List, Dict

from commands.bus_stop import BusStopCommands
from commands.bus import BusCommands
from config import BUS_DIR


class Bus(pykka.ThreadingActor):
    def __init__(self, size: int, number: str, bus_stops: List[pykka.ActorRef]):
        self.size = size
        self.number = number

        self.current_bus_stop: Optional[pykka.ActorRef] = None
        self.bus_stops = self._bus_stops_generator(bus_stops)

        self._logger = self.setup_logging()

        self._logger.info(f'Bus {self.number} with size {self.size} is on track!')
        super(Bus, self).__init__()

    def on_receive(self, message: Dict[str, BusStopCommands]):
        resp = message.get('command')

        if resp == BusStopCommands.REJECT_BUS:
            self.current_bus_stop = next(self.bus_stops)
            self._logger.info(
                f'{self.number} with size {self.size} is moving to {self.current_bus_stop.proxy().name.get()}')
            time.sleep(random.randint(10, 15))
            self.current_bus_stop.tell({'command': BusCommands.REQUEST_FOR_STOP, 'sender': self})

        if resp == BusStopCommands.ACCEPT_BUS:
            self._logger.info(f'{self.number} accepting passengers...')
            time.sleep(random.randint(5, 10))
            self.current_bus_stop.tell({'command': BusCommands.REQUEST_FOR_LEAVE, 'sender': self})

            self.on_start()

    def on_start(self) -> None:
        bus_stop = next(self.bus_stops)
        self._logger.info(f'{self.number} with size {self.size} is moving to {bus_stop.proxy().name.get()}...')
        time.sleep(random.randint(5, 10))
        self._logger.info(f'{self.number} has arrived to {bus_stop.proxy().name.get()}')
        self.current_bus_stop = bus_stop
        bus_stop.tell({'command': BusCommands.REQUEST_FOR_STOP, 'sender': self})

    def __str__(self):
        return f'Bus {self.number} with size {self.size}'

    @staticmethod
    def _bus_stops_generator(bus_stops):
        while True:
            for bs in bus_stops:
                yield bs

    def setup_logging(self):
        logger = logging.getLogger(self.number)
        logger.setLevel('INFO')
        fh = logging.FileHandler(BUS_DIR / (self.number + '.log'))
        fh.setLevel('INFO')
        logger.addHandler(fh)
        return logger
