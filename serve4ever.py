""" Prwto deigma"""

from __future__ import print_function
from gevent.server import StreamServer

class Super:
    def __init__(self):
        self.name = 'Super Class'

    def process(self):
        print("Data processed!")
        #raise NotImplementedError('Class %s must implement the process method' % self.__class__.__name__)


class Child(Super):
    def process(self):
        print("Do anything you want with the data!")



# this handler will be run for each incoming connection in a dedicated greenlet
def senddata(socket, address):
    print('New connection from %s:%s' % address)
    socket.sendall(b'Data comes, doing process again.\r\n')

    ss = Child()
    ss.process()



if __name__ == '__main__':
    # to make the server use SSL, pass certfile and keyfile arguments to the constructor
    server = StreamServer(('0.0.0.0', 16000), senddata)

    # to start the server asynchronously, use its start() method;
    # we use blocking serve_forever() here because we have no other jobs
    print('Starting data server on port 16000')
    server.serve_forever()