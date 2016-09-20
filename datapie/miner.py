from __future__ import print_function

import gevent
from datapie.typings import Address, ResultsDict
from datapie.utils import ClassPrint
from gevent.queue import Queue
from gevent.server import StreamServer


class Miner(StreamServer, ClassPrint):
    def __init__(self, listener: Address, mine: Address, **ssl_args):
        super(Miner, self).__init__(listener, **ssl_args)
        self.results = {}  # type: ResultsDict
        self.mine_address = mine
        gevent.spawn(self._connect_and_start_receiving)

    def handle(self, socket, address):
        self.print('New connection from %s:%s' % address)
        socket.sendall(b'Welcome to the miner! We will send you processed data\r\n')
        # add to listeners after the welcoming message
        self.add_to_listeners(address)
        while True:
            # get current listener's queue
            q = self.results[address]
            if q.empty():
                # sleep to allow other handlers to run
                gevent.sleep(0)
                continue
            # get result from queue
            result = q.get()
            # send result
            try:
                socket.sendall(result)
            except ConnectionError:
                # remove from listeners
                self.remove_from_listeners(address)
                # exit
                break

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
            self.set_result(processed)
        rfileobj.close()
        sock.close()

    def add_to_listeners(self, address: Address):
        self.print('adding to listeners %s:%s' % address)
        self.results[address] = Queue()

    def remove_from_listeners(self, address: Address):
        self.print('removing from listeners %s:%s' % address)
        self.results.pop(address)

    def set_result(self, result):
        for queue in self.results.values():
            queue.put(result)

    def process(self, data: bytes) -> bytes:
        raise NotImplementedError('Class %s must implement the process method' % self.__class__.__name__)

    @staticmethod
    def _connect_to_mine(address):
        return gevent.socket.create_connection(address)
