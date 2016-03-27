from context import styrobot 

class MockPlugin(styrobot.Plugin):
    def initialize(self):
        print('POOOP')

obj = MockPlugin()
obj.initialize()
