from io import BufferedReader
class Gen5Save:
    def __init__(self, data):
        if isinstance(data, BufferedReader):
            data.seek(0x19404)
            tname = data.read(7)
            # Now we need to do some post processing
            tname = tname.strip(b"\x00") # Strip \x00
            tname = tname.strip(b"\xff") # Strip \xff
            outstring = b""
            for b in tname: # Strip the \x00s inbetween letters
                byte = b.to_bytes(1, 'little')
                if byte != b"\x00":
                    outstring = outstring + byte
            # Now we make it a string.
            tname = str(outstring)[2:-1] # The [2:-1] part strips the annoying b"" things from the string
            self.trainer_name = tname
        elif isinstance(data, bytes):
            self._data = data
        elif isinstance(data, bytearray):
            self._data = data
        
