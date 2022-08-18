"""
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
"""
BASE_RESPONSE = b"\x00\x00\x00\x00" + (b"\x00" * 0x7C)
END_RESPOSNE = b"\xFF" * 0x40
PLAYSTATUS = "account.playstatus"  # Called when you perform Game Sync
SLEEPILY_BITLIST = "sleepily.bitlist"  # List of banned species
SAVEDATA_GETBW = "savedata.getbw"  # B2W2 Memory Link
SAVEDATA_DOWNLOAD = "savedata.download"  # self-explanatory
WORLDBATTLE_DOWNLOAD = (
    "worldbattle.download"  # Click Battle Competition>Wi-Fi Competition>Participate
)
ACCOUNT_CREATEDATA = "account.createdata"  # Unused
ACCOUNT_CREATE_UPLOAD = (
    "account.create.upload"  # Upload savedata, alias to savedata.upload
)
SAVEDATA_UPLOAD = "savedata.upload"  # self-explanatory
WORLDBATTLE_UPLOAD = "worldbattle.upload"  # ???
SAVEDATA_DOWNLOAD_FINISH = "savedata.download.finish"  # likely telling the server that savedata download is done
DREAMING_POKEMON_RESPONSE = b"\x00" * 0x4
SLEEPILY_INTERNAL_SERVER_ERROR = b"\xf0\xff\x00\x00"
SLEEPILY_HIGH_TRAFFIC_VOLUMES = b"\xf1\xff\x00\x00"
SLEEPILY_UNDERGOING_MAINTAINCE = b"\xf2\xff\x00\x00"
UNKNOWN_RESPONSE_1 = b"\x01" * 0x4
WAKE_UP_AND_DOWNLOAD = BASE_RESPONSE + b"\x03" * 0x4 + END_RESPOSNE
WAKE_UP_RESPONSE = (
    b"\x04" * 0x4
)  # 0x40 will work too, as long as you remove the BASE_RESPONSE and END_RESPONSE
OLD_WAKE_UP_RESPONSE = b"\x04" * 0x40
PUT_POKE_TO_SLEEP_RESPONSE = BASE_RESPONSE + b"\x05" * 4 + END_RESPOSNE
CREATE_ACCOUNT = BASE_RESPONSE + b"\x08" * 0x4 + END_RESPOSNE
OLD_CREATE_ACCOUNT = b"\x08" * 0x40
WHITE_1_ROMCODE = 20
BLACK_1_ROMCODE = 21
WHITE_2_ROMCODE = 22
BLACK_2_ROMCODE = 23
