# --- Constants ---
PLAYSTATUS = "account.playstatus" # Likely checking if you can play dreamworld at the moment
SLEEPILY_BITLIST = "sleepily.bitlist" # ???
SAVEDATA_GETBW = "savedata.getbw" # Likely checking if it's Black or White
SAVEDATA_DOWNLOAD = "savedata.download" # self-explanatory
WORLDBATTLE_DOWNLOAD = "worldbattle.download" # Click Battle Competition>Wi-Fi Competition>Participate
ACCOUNT_CREATEDATA = "account.createdata" # Likely what happens when you pick "Game Sync Settings" on title screen
ACCOUNT_CREATE_UPLOAD = "account.create.upload" # ???
SAVEDATA_UPLOAD = "savedata.upload" # self-explanatory
WORLDBATTLE_UPLOAD = "worldbattle.upload" # ???
SAVEDATA_DOWNLOAD_FINISH = "savedata.download.finish" # likely telling the server that savedata download is done
DREAMING_POKEMON_RESPONSE = b"\x00" * 0x40
UNKNOWN_RESPONSE_1 = b"\x01" * 0x40
WAKE_UP_AND_DOWNLOAD = b"\x03" * 0x40
WAKE_UP_RESPONSE = b"\x04" * 0x40
PUT_POKE_TO_SLEEP_RESPONSE = b"\x00\x00\x00\x00" + (b"\x00" * 0x7c) + b"\x05" * 4 + b"\xFF" * 0x40
CREATE_ACCOUNT = b"\x08" * 0x40
BASE_RESPONSE = b"\x00" * 0x7c + b"\x00" * 4 + b"\x03" + b"\x00" * 0x3
#UNKNOWN_RESPONSE_2 = b"\x09" * 0x40 Just a test, the DS will error if it recives this

# --- Imports ---
from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from uuid import uuid1
from os.path import exists
# --- Key Definitions ---
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///victini.db' # The DB is named "Victini" after the Pokemon and for pretty much no reason
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# --- Model Imports ---
import models
# --- Routes ---
@app.route("/dsio/gw", methods=["GET", "POST"])
def gw():
    if request.args["p"] == PLAYSTATUS:
        if exists(f"savdata-{request.args['gsid']}.sav"): # Check if trainer has registered with the server
            return b"\x00\x00\x00\x00" + (b"\x00" * 0x7c) + b"\x05" * 4 + b"\xFF" * 0x40
        return b"\x08"
    elif request.args["p"] == SAVEDATA_UPLOAD: # Triggered by putting a Pokemon to sleep.
        # Dump
        with open(f"savdata-{request.args['gsid']}.sav", "wb") as f:
            f.write(request.get_data())
        return DREAMING_POKEMON_RESPONSE
    elif request.args["p"] == ACCOUNT_CREATE_UPLOAD:
        with open(f"savdata-{request.args['gsid']}.sav", "wb") as f:
            f.write(request.get_data())
        return DREAMING_POKEMON_RESPONSE # Success response
    elif request.args["p"] == WORLDBATTLE_DOWNLOAD: # Live competition
        if exists(f"savdata-{request.args['gsid']}.sav"):
            return Response("no", status=403) # The server is undergoing maintaince
        return DREAMING_POKEMON_RESPONSE # A.k.a "Please use Game Sync Settings"
    else:
        return DREAMING_POKEMON_RESPONSE


# --- Main Block ---
if __name__ == "__main__":
    app.run(host="0.0.0.0")
