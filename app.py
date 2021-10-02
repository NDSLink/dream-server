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
# --- Imports ---
from flask import Flask, request, jsonify
# --- Key Definitions ---
app = Flask(__name__)
# --- Routes ---
@app.route("/dsio/gw")
def gw():
    return b"\x00" * 0x40


# --- Main Block ---
if __name__ == "__main__":
    app.run(host="0.0.0.0")