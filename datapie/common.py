from __future__ import print_function

import gevent
from datapie.typings import Address
from datapie.typings import ListenersDict
from gevent.queue import Queue
from gevent.server import StreamServer


class ClassPrefix:
    def print(self, msg, **kwargs):
        print(self.prefix_str(msg), **kwargs)

    def prefix_str(self, msg: str) -> str:
        return '%s: %s' % (self.__class__.__name__, msg)


class BaseServer(StreamServer, ClassPrefix):
    """
    A simple StreamServer that stores listeners to a dictionary and a queue for each one.
    The handle will automatically get from the queue as soon as data are available.
    To add data to the queue use the set_data method.
    """
    def __init__(self, listener: Address, welcoming_msg: str=None, **ssl_args):
        super(BaseServer, self).__init__(listener, **ssl_args)
        self.listeners = {}  # type: ListenersDict
        self.welcoming_msg = (welcoming_msg or 'Welcome to the %s server! We transfer you data.' % self.__class__.__name__) + '\r\n'
        # do we really need to send bytes?
        self.welcoming_msg = self.welcoming_msg.encode()

    def handle(self, socket, address: Address):
        self.print('New connection from %s:%s' % address)
        socket.sendall(self.welcoming_msg)
        # add to listeners after the welcoming message
        self._add_to_listeners(address)
        while True:
            # get current listener's queue
            q = self.listeners[address]
            if q.empty():
                # sleep to allow other handlers to run
                gevent.sleep(0)
                continue
            # get result from queue
            data = q.get()
            # send result
            try:
                socket.sendall(data)
            except ConnectionError:
                # remove from listeners
                self._remove_from_listeners(address)
                # exit
                break

    def _add_to_listeners(self, address: Address):
        self.print('adding to listeners %s:%s' % address)
        self.listeners[address] = Queue()

    def _remove_from_listeners(self, address: Address):
        self.print('removing from listeners %s:%s' % address)
        self.listeners.pop(address)

    def set_data(self, result):
        for queue in self.listeners.values():
            queue.put(result)
