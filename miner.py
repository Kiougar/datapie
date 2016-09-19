from __future__ import print_function
from gevent.server import StreamServer
from typing import Tuple
Address = Tuple[str, int]


class Miner(StreamServer):
    def __init__(self, listener: Address, **ssl_args):
        super(Miner, self).__init__(listener, **ssl_args)

    def handle(self, socket, address):
        print('New connection from %s:%s' % address)
        # using a makefile because we want to use readline()
        rfileobj = socket.makefile(mode='rb')
        while True:
            line = rfileobj.readline()
            if not line:
                print("client disconnected")
                break
            if line.strip().lower() == b'quit':
                print("client quit")
                break
            print("received %r" % line)
            processed = self.process(line)
            socket.sendall(b'%s>' % processed)
        rfileobj.close()

    def process(self, data: bytes) -> bytes:
        raise NotImplementedError('Class %s must implement the process method' % self.__class__.__name__)
