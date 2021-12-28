import logging

import pykka
from typing import TYPE_CHECKING, Dict, Union

from commands.bus_stop import BusStopCommands
from commands.bus import BusCommands
from config import BUS_STOP_DIR

if TYPE_CHECKING:
    from .bus import Bus


class BusStop(pykka.ThreadingActor):
    def __init__(self, name: str, max_size: int = 10):
        self.max_size = max_size
        self.current_size = 0

        self.name = name
        self.busses: Dict[str, 'Bus'] = {}

        self._logger = self.setup_logging()

        super(BusStop, self).__init__()

    def on_receive(self, message: Dict[str, Union[int, BusCommands, 'Bus']]):
        command, sender = message.get('command'), message.get('sender')

        if command == BusCommands.REQUEST_FOR_STOP:
            self.handle_request_for_stop(sender)

        if command == BusCommands.REQUEST_FOR_LEAVE:
            self.handle_request_for_leave(sender)

    def handle_request_for_stop(self, sender: 'Bus'):

        if sender.number in self.busses.keys():
            sender.actor_ref.tell({'command': BusStopCommands.COMMAND_FAIL})

        elif sender.size + self.current_size > 10:
            sender.actor_ref.tell({'command': BusStopCommands.REJECT_BUS})
            self._logger.info(f'{self.name} rejected bus {sender.number} with size {sender.size}')

        else:
            self.busses[sender.number] = sender
            self.current_size += sender.size
            sender.actor_ref.tell({'command': BusStopCommands.ACCEPT_BUS})
            self._logger.info(f'{self.name} accepted bus {sender.number} with size {sender.size}. '
                              f'Current bus stop size: {self.current_size}')

    def handle_request_for_leave(self, sender: 'Bus'):
        if sender.number not in self.busses.keys():
            sender.actor_ref.tell({'command': BusStopCommands.COMMAND_FAIL})
        else:
            del self.busses[sender.number]
            self.current_size -= sender.size
            self._logger.info(f'{sender.number} with size {sender.size} has left {self.name}. '
                              f'Current bus stop size: {self.current_size}')

    def setup_logging(self):
        logger = logging.getLogger(self.name)
        logger.setLevel('INFO')
        fh = logging.FileHandler(BUS_STOP_DIR / (self.name + '.log'))
        fh.setLevel('INFO')
        logger.addHandler(fh)
        return logger
