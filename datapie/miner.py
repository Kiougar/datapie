from __future__ import print_function

import gevent
from datapie.typings import Address, ResultsDict
from gevent.queue import Queue
from gevent.server import StreamServer


class Miner(StreamServer):
    def __init__(self, listener: Address, mine: Address, **ssl_args):
        def connect_to_mine(address):
            return gevent.socket.create_connection(address)

        super(Miner, self).__init__(listener, **ssl_args)
        self.mine_address = mine
        self.mine_socket = connect_to_mine(mine)
        self.results = {}  # type: ResultsDict
        gevent.spawn(self.mine_handle)

    def handle(self, socket, address):
        print('New connection from %s:%s' % address)
        socket.sendall(b'Welcome to the miner! We will send you processed data\r\n')
        self.add_to_listeners(address)
        while True:
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
            except (ConnectionError, ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError):
                self.remove_from_listeners(address)
                break

    def mine_handle(self):
        sock = self.mine_socket
        rfileobj = sock.makefile(mode='rb')
        while True:
            line = rfileobj.readline()
            if not line:
                print('Mine disconnected')
                break
            print('received %r' % line)
            processed = self.process(line)
            self.set_result(processed)
        rfileobj.close()
        sock.close()

    def add_to_listeners(self, address: Address):
        print('adding to listeners %s:%s' % address)
        self.results[address] = Queue()

    def remove_from_listeners(self, address: Address):
        print('removing from listeners %s:%s' % address)
        self.results.pop(address)

    def set_result(self, result):
        for queue in self.results.values():
            queue.put(result)

    def process(self, data: bytes) -> bytes:
        raise NotImplementedError('Class %s must implement the process method' % self.__class__.__name__)
