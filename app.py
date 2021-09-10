# --- Typing Imports ---
from typing import Final
# --- Constants ---
PLAYSTATUS: Final[str] = "account.playstatus"
SLEEPILY_BITLIST: Final[str] = "sleepily.bitlist"
SAVEDATA_GETBW: Final[str] = "savedata.getbw"
SAVEDATA_DOWNLOAD: Final[str] = "savedata.download"
WORLDBATTLE_DOWNLOAD: Final[str] = "worldbattle.download"
ACCOUNT_CREATEDATA: Final[str] = "account.createdata"
ACCOUNT_CREATE_UPLOAD: Final[str] = "account.create.upload"
SAVEDATA_UPLOAD: Final[str] = "savedata.upload"
WORLDBATTLE_UPLOAD: Final[str] = "worldbattle.upload"
SAVEDATA_DOWNLOAD_FINISH: Final[str] = "savedata.download.finish"
# --- Imports ---
from flask import Flask, request, jsonify
# --- Key Definitions ---
app = Flask(__name__)
# --- Routes ---
@app.route("/<route>", methods=["GET", "POST"])
def route(route: str) -> str:
    print(f"Request to {route}")
    print(f"Command: {request.args['p']}")
    try:
        print(f"JSON: {request.get_json()}")
    except:
        print("No JSON")
# --- Main Block ---
if __name__ == "__main__":
    app.run(host="0.0.0.0")