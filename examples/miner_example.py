import random
import string

import gevent
from datapie import Mine
from datapie import Miner


class MyMiner(Miner):
    def process(self, data: bytes):
        return data.upper()


class MyMine(Mine):
    @staticmethod
    def random_word(size):
        return ''.join(random.choice(string.ascii_letters) for _ in range(size))

    def get_data(self):
        gevent.sleep(3)
        return (self.random_word(10).lower() + '\r\n').encode()


if __name__ == '__main__':
    mine = MyMine(('127.0.0.1', 16000))
    print('Starting MyMine on port 16000')
    mine.start()

    # TODO miner must indefinitely try to connect to the mine
    miner = MyMiner(('127.0.0.1', 16001), mine.address)
    print('Starting MyMiner on port 16001')
    miner.serve_forever()
