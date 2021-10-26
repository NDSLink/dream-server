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
            """
            data.seek(0x1D309)  # Sleeping Pokemon Data.
            pkm = data.read(220)
            checksum = int.from_bytes(pkm[0x06:0x07], "little")
            pid = pkm[0x00:0x03]
            rng = lambda x: 0x41C64E6D * x + 0x6073
            finished = [0] * 0x7
            for y in range(0x08, 0x87, 0x2):
                decrypted = (int.from_bytes(pkm[y : y + 1], 'little') ^ rng(checksum))
                decrypted = decrypted.to_bytes(4, 'little')
                finished.append(decrypted[1])
                finished.append(decrypted[2])
            shift = ((pid & 0x3E000) >> 0xD) % 24
            A = 0x08
            B = 0x28
            C = 0x48
            D = 0x68
            shift_cols = [
                C,
                D,
                B,
                D,
                C,
                C,
                B,
                A,
                B,
                A,
                D,
                A,
                C,
                B,
                D,
                A,
                D,
                A,
                B,
                C,
                B,
                A,
                C,
                A,
                B,
            ]  # location of block C
            nick_location = shift_cols[shift]
            nick = str((b"".join(finished)[nick_location : nick_location + 10]))[2:-1]
            self.sleeping_pokemon_nick = nick
            """

        elif isinstance(data, (bytes, bytearray)):
            self._data = data
            tid = data[0x19414 : 0x19414 + 2]  # TID is a 32-bit integer
            self.tid = int.from_bytes(tid, "little")
            tname = self._parse_tname(data)
            if tname == b"":
                tname = self._parse_tname(data, True)  # Obtain data from mirror
            self.trainer_name = tname
