from .miner import Miner


class MyMiner(Miner):
    def process(self, data: bytes):
        print('%s: upper casing data "%s"' % (self.__class__.__name__, data))
        return data.upper()


if __name__ == '__main__':
    """
    Connect to it with:
    telnet localhost 16000

    Terminate the connection by terminating telnet (typically Ctrl-] and then 'quit').
    """
    miner = MyMiner(('127.0.0.1', 16000))

    print('Starting MyMiner on port 16000')
    miner.serve_forever()
