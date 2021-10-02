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
# --- Imports ---
from flask import Flask, request, jsonify
# --- Key Definitions ---
app = Flask(__name__)
# --- Routes ---
@app.route("/")
@app.route("/<route>", methods=["GET", "POST"])
def route(route: str="test") -> str:
    print(f"Request to {route}")
    print(f"Command: {request.args['p']}")
    try:
        print(f"JSON: {request.get_json()}")
    except:
        print("No JSON")
# --- Main Block ---
if __name__ == "__main__":
    app.run(host="0.0.0.0")
