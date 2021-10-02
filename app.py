# --- Constants ---
PLAYSTATUS = "account.playstatus"
SLEEPILY_BITLIST = "sleepily.bitlist"
SAVEDATA_GETBW = "savedata.getbw"
SAVEDATA_DOWNLOAD = "savedata.download"
WORLDBATTLE_DOWNLOAD = "worldbattle.download"
ACCOUNT_CREATEDATA = "account.createdata"
ACCOUNT_CREATE_UPLOAD = "account.create.upload"
SAVEDATA_UPLOAD = "savedata.upload"
WORLDBATTLE_UPLOAD = "worldbattle.upload"
SAVEDATA_DOWNLOAD_FINISH = "savedata.download.finish"
DREAMING_POKEMON_RESPONSE = b"\x00" * 0x40
UNKNOWN_RESPONSE_1 = b"\x01" * 0x40
WAKE_UP_AND_DOWNLOAD = b"\0x3" * 0x40
WAKE_UP_RESPONSE = b"\x04" * 0x40
UNKNOWN_RESPONSE_2 = b"\x09" * 0x40
# --- Imports ---
from flask import Flask, request, jsonify
# --- Key Definitions ---
app = Flask(__name__)
# --- Routes ---
@app.route("/dsio/gw", methods=["GET", "POST"])
def gw():
    if request.args["p"] == PLAYSTATUS:
        return b"\x05"
    else:
        return DREAMING_POKEMON_RESPONSE


# --- Main Block ---
if __name__ == "__main__":
    app.run(host="0.0.0.0")