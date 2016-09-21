import random
import string

import gevent
from datapie import Mine
from datapie import Miner


class MyMiner1(Miner):
    def process(self, data: bytes):
        return data.upper()


class MyMiner2(Miner):
    def process(self, data: bytes):
        return data.lower()


class MyMine(Mine):
    @staticmethod
    def random_word(size):
        return ''.join(random.choice(string.ascii_letters) for _ in range(size))

    def get_data(self):
        gevent.sleep(3)
        return (self.random_word(10).lower() + '\r\n').encode()


if __name__ == '__main__':
    mine = MyMine(('127.0.0.1', 16000))
    miner1 = MyMiner1(('127.0.0.1', 16001), mine.address)
    miner2 = MyMiner2(('127.0.0.1', 16002), miner1.address)

    print('Starting MyMiner2 on port 16002')
    miner2.start()

    # delay the miner by 10 seconds to check that miner2 can connect to it successfully
    gevent.sleep(10)
    print('Starting MyMiner1 on port 16001')
    miner1.start()

    # delay the mine by 20 seconds to check that miner can connect to it successfully even if it was started later on
    gevent.sleep(10)
    print('Starting MyMine on port 16000...')
    mine.serve_forever()
