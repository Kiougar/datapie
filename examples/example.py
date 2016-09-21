class Super:
    def __init__(self):
        self.name = 'Super Class'

    def run(self):
        self.process()

    def process(self):
        raise NotImplementedError('Class %s must implement the process method' % self.__class__.__name__)


class SubSuper(Super):
    def process(self):
        print(self.name)


class WrongSubSuper(Super):
    pass


if __name__ == '__main__':
    # This will run normally
    ss = SubSuper()
    ss.run()

    # The following will raise an error because the process method is not implemented by the sub class
    ws = WrongSubSuper()

