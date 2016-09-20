from __future__ import print_function

from datapie.typings import Address
from datapie.utils import ClassPrint
from gevent.server import StreamServer


class Mine(StreamServer, ClassPrint):
    def __init__(self, listener: Address, **ssl_args):
        super(Mine, self).__init__(listener, **ssl_args)
        # TODO we need to spawn here a method that fetches data and stores them to a Queue, similar to Miner, so that it is sent to all listeners

    def handle(self, socket, address: Address):
        self.print('New connection from %s:%s' % address)
        socket.sendall(b'Welcome to the Mine server! We transfer you data.\r\n')
        # TODO store listeners here, similar to Miner

        while True:
            # TODO the data need to be received from the Queue
            data = self.get_data()
            socket.sendall(data)

    def get_data(self):
        raise NotImplementedError('Class %s must implement the process method' % self.__class__.__name__)
