from __future__ import print_function

import gevent
from datapie.typings import Address
from datapie.common import BaseServer


class Mine(BaseServer):
    def __init__(self, listener: Address, **ssl_args):
        welcoming_msg = 'Welcome to the Mine server. We send you data!'
        super(Mine, self).__init__(listener, welcoming_msg, **ssl_args)
        gevent.spawn(self._start_storing)

    def get_data(self):
        raise NotImplementedError('Class %s must implement the process method' % self.__class__.__name__)

    def _start_storing(self):
        while True:
            # get data from the overridden get_data method
            data = self.get_data()
            self.set_data(data)
