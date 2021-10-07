from io import BufferedReader
class Gen5Save:
    def __init__(self, data):
        if isinstance(data, BufferedReader):
            data.seek(0x19404)
            tname = data.read(16) # TODO: is this actually the proper trainer name length
            self.trainer_name = tname
        elif isinstance(data, bytes):
            self._data = data
        elif isinstance(data, bytearray):
            self._data = data
        
