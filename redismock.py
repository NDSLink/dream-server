# dumb solution for testing on Windows, since Windows doesn't have (proper) Redis.

class DummyRedis:
    def __init__(self, *args, **kwargs):
        pass
    def publish(self, *args, **kwargs):
        pass