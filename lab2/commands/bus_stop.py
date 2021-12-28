import enum


class BusStopCommands(enum.IntEnum):
    REJECT_BUS = 1
    ACCEPT_BUS = 2

    COMMAND_FAIL = 3
