from __future__ import print_function

import gevent
import random
import string
from datapie.typings import Address
from datapie.utils import ClassPrint
from gevent.server import StreamServer
from gevent.queue import Queue


class Mine(StreamServer, ClassPrint):
    def __init__(self, listener: Address, **ssl_args):
        super(Mine, self).__init__(listener, **ssl_args)
        self.listeners = {}
        gevent.spawn(self.receive_and_storing)
        # TODO we need to spawn here a method that fetches data and stores them to a Queue, similar to Miner, so that it is sent to all listeners

    def handle(self, socket, address: Address):
        self.print('New connection from %s:%s' % address)
        socket.sendall(b'Welcome to the Mine server! We transfer you data.\r\n')
        # add to listeners after the welcoming message
        self.add_to_listeners(address)
        # TODO store listeners here, similar to Miner

        while True:
            # TODO the data need to be received from the Queue

            # get current listener's queue
            q = self.listeners[address]
            if q.empty():
                # sleep to allow other handlers to run
                gevent.sleep(0)
                continue
            # get result from queue
            data = q.get().encode()
            # send result

            try:
                socket.sendall(data)
            except ConnectionError:
                # remove from listeners
                self.remove_from_listeners(address)
                # exit
                break

    def get_data(self):
        raise NotImplementedError('Class %s must implement the process method' % self.__class__.__name__)


    def add_to_listeners(self, address: Address):
        self.print('adding to listeners %s:%s' % address)
        self.listeners[address] = Queue()

    def remove_from_listeners(self, address: Address):
        self.print('removing from listeners %s:%s' % address)
        self.listeners.pop(address)

    def set_data(self, result):
        for queue in self.listeners.values():
            queue.put(result)

    def receive_and_storing(self):

        while True:
            gevent.sleep(3)
            data = ''.join(random.choice(string.ascii_letters) for _ in range(10))
            # den kserw apo pou tha pairnei data to mine opote eftiaksa merika
            self.print(data)

            self.set_data(data)

# gia na to testarw
if __name__ == '__main__':
    mine = Mine(('127.0.0.1', 16000))
    print('Starting MyMine on port 16000...')
    mine.serve_forever()
