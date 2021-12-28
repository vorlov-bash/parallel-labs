from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent

LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

BUS_STOP_DIR = LOG_DIR / 'bus_stops'
BUS_STOP_DIR.mkdir(exist_ok=True)

BUS_DIR = LOG_DIR / 'bus'
BUS_DIR.mkdir(exist_ok=True)
