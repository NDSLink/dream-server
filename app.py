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
WAKE_UP_RESPONSE = b"\x04" * 0x40
# --- Imports ---
from flask import Flask, request, jsonify
# --- Key Definitions ---
app = Flask(__name__)
# --- Routes ---
@app.route("/dsio/gw")
def gw():
    if request.args["p"] == PLAYSTATUS:
        return DREAMING_POKEMON_RESPONSE
    else:
        return WAKE_UP_RESPONSE


# --- Main Block ---
if __name__ == "__main__":
    app.run(host="0.0.0.0")