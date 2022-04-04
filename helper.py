from io import BufferedReader


class Gen5Save:
    def _parse_tname(self, data, mirror=False):
        if mirror:
            loc = 0x23F36
        else:
            loc = 0x19404
        tname = data[loc : loc + 7]
        # Now we need to do some post processing
        tname = tname.strip(b"\x00")  # Strip \x00
        tname = tname.strip(b"\xff")  # Strip \xff
        outstring = b""
        for b in tname:  # Strip the \x00s inbetween letters
            byte = b.to_bytes(1, "little")
            if byte != b"\x00":
                outstring = outstring + byte
        # Now we make it a string.
        tname = str(outstring)[
            2:-1
        ]  # The [2:-1] part strips the annoying b"" things from the string
        return tname

    def __init__(self, data):
        if isinstance(data, BufferedReader):
            self._data = data.read()
            data.seek(0x19404)
            tname = data.read(14)
            tname.strip(b"\xff")
            # Now we need to do some post processing
            outstring = b""
            for b in tname:  # Strip the \x00s inbetween letters
                byte = b.to_bytes(1, "little")
                if byte != b"\x00" and byte != b"\xff":
                    outstring = outstring + byte
            # Now we make it a string.
            tname = str(outstring)[
                2:-1
            ]  # The [2:-1] part strips the annoying b"" things from the string
            data.seek(0x19414)
            tid = data.read(2)  # TID is a 32-bit integer
            self.tid = int.from_bytes(tid, "little")
            self.trainer_name = tname
            data.seek(0x19419)
            self.gamever = 0 if data.read(1) == 0x44 else 1

        elif isinstance(data, (bytes, bytearray)):
            self._data = data
            tid = data[0x19414 : 0x19414 + 2]  # TID is a 32-bit integer
            self.tid = int.from_bytes(tid, "little")
            self.gamever = 0 if data[0x19419] == 0x44 else 1  # 0 = white, 1 = black
            tname = self._parse_tname(data)
            if tname == b"":
                tname = self._parse_tname(data, True)  # Obtain data from mirror
            self.trainer_name = tname
