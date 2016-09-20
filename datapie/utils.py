class ClassPrint:
    def print(self, msg, **kwargs):
        print('%s: %s' % (self.__class__.__name__, msg), **kwargs)
