import abc

class Plugin:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def initialize(self): pass
