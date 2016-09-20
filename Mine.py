
from __future__ import print_function
from gevent.server import StreamServer
from typing import Tuple
Address = Tuple[str, int]

import random, string, time


class Mine(StreamServer):
    def __init__(self, listener: Address, **ssl_args):
        super(Mine, self).__init__(listener, **ssl_args)

    def randomword(self, size):
        return ''.join(random.choice(string.ascii_letters) for i in range(size))


    def handle(self, socket, address):
        print('New connection from %s:%s' % address)
        socket.sendall(b'Welcome to the Mine server! We transfer you data.\r\n')

        while True:

            time.sleep(3)
            rstring = self.randomword(10)
            socket.sendall(rstring.encode())



if __name__ == '__main__':

    mine = Mine(('127.0.0.1', 16100))

    # to start the server asynchronously, use its start() method;
    # we use blocking serve_forever() here because we have no other jobs
    print('Starting Mine on port 16100')
    mine.serve_forever()