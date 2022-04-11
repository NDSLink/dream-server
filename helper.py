'''
MIT License

Copyright (c) 2022 DSLink Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
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
