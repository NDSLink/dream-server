# --- Constants ---
PLAYSTATUS = "account.playstatus" # Likely checking if you can play dreamworld at the moment
SLEEPILY_BITLIST = "sleepily.bitlist" # ???
SAVEDATA_GETBW = "savedata.getbw" # Likely checking if it's Black or White
SAVEDATA_DOWNLOAD = "savedata.download" # self-explanatory
WORLDBATTLE_DOWNLOAD = "worldbattle.download" # ???
ACCOUNT_CREATEDATA = "account.createdata" # Likely what happens when you pick "Game Sync Settings" on title screen
ACCOUNT_CREATE_UPLOAD = "account.create.upload" # ???
SAVEDATA_UPLOAD = "savedata.upload" # self-explanatory
WORLDBATTLE_UPLOAD = "worldbattle.upload" # ???
SAVEDATA_DOWNLOAD_FINISH = "savedata.download.finish" # likely telling the server that savedata download is done
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
