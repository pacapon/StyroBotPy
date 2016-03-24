import abc

class StryoModule:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def initialize(self): pass
