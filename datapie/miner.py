from __future__ import print_function

import gevent
from datapie.common import BaseServer
from datapie.typings import Address


class Miner(BaseServer):
    def __init__(self, listener: Address, mine: Address, **ssl_args):
        welcoming_msg = 'Welcome to the Miner server. We send you processed data!'
        super(Miner, self).__init__(listener, welcoming_msg, **ssl_args)
        self.mine_address = mine
        gevent.spawn(self._connect_and_start_receiving)

    def _connect_and_start_receiving(self):
        self.mine_socket = None
        while self.mine_socket is None:
            try:
                self.print('trying to connect to %s:%s ...' % self.mine_address)
                self.mine_socket = self._connect_to_mine(self.mine_address)
                sock_name = self.mine_socket.getsockname()  # type: Address
                self.print('successfully connected to %s:%s using %s:%s' % (self.mine_address + sock_name))
            except ConnectionError as e:
                self.print('%s %s' % (e.__class__.__name__, e.strerror))
                continue
        self._start_receiving()

    def _start_receiving(self):
        sock = self.mine_socket
        rfileobj = sock.makefile(mode='rb')
        while True:
            line = rfileobj.readline()
            if not line:
                self.print('sender disconnected')
                break
            self.print('received %r' % line)
            processed = self.process(line)
            self.set_data(processed)
        rfileobj.close()
        sock.close()

    def process(self, data: bytes) -> bytes:
        raise NotImplementedError('Class %s must implement the process method' % self.__class__.__name__)

    @staticmethod
    def _connect_to_mine(address):
        return gevent.socket.create_connection(address)
