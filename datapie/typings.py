from typing import Tuple, Dict
from gevent.queue import Queue

Address = Tuple[str, int]
ListenersDict = Dict[Address, Queue]
