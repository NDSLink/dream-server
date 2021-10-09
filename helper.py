from io import BufferedReader
class Gen5Save:
    def __init__(self, data):
        if isinstance(data, BufferedReader):
            self._data = data.read()
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
            data.seek(0x19414)
            tid = data.read(2) # TID is a 32-bit integer
            self.tid = int.from_bytes(tid, 'little')
            self.trainer_name = tname
        elif isinstance(data, (bytes, bytearray)):
            self._data = data
            tname = data[0x19404:0x19404+7]
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
            tid = data[0x19414:0x19414+2] # TID is a 32-bit integer
            self.tid = int.from_bytes(tid, 'little')
            self.trainer_name = tname
        
