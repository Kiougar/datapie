from __future__ import print_function

from datapie.typings import Address
from gevent.server import StreamServer


class Mine(StreamServer):
    def __init__(self, listener: Address, **ssl_args):
        super(Mine, self).__init__(listener, **ssl_args)

    def handle(self, socket, address):
        print('New connection from %s:%s' % address)
        socket.sendall(b'Welcome to the Mine server! We transfer you data.\r\n')

        while True:
            data = self.get_data()
            socket.sendall(data)

    def get_data(self):
        raise NotImplementedError('Class %s must implement the process method' % self.__class__.__name__)
