# --- Constants ---
BASE_RESPONSE = b"\x00\x00\x00\x00" + (b"\x00" * 0x7c)
END_RESPOSNE = b"\xFF" * 0x40
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
DREAMING_POKEMON_RESPONSE = b"\x00" * 0x4
UNKNOWN_RESPONSE_1 = b"\x01" * 0x4
WAKE_UP_AND_DOWNLOAD = b"\x03" * 0x4
WAKE_UP_RESPONSE = b"\x04" * 0x4 # 0x40 will work too, as long as you remove the BASE_RESPONSE and END_RESPONSE
OLD_WAKE_UP_RESPONSE = b"\x04" * 0x40 # Either seems to work?
PUT_POKE_TO_SLEEP_RESPONSE = BASE_RESPONSE + b"\x05" * 4 + END_RESPOSNE
CREATE_ACCOUNT = BASE_RESPONSE + b"\x08" * 0x4 + END_RESPOSNE
OLD_CREATE_ACCOUNT = b"\x08" * 0x40

#UNKNOWN_RESPONSE_2 = b"\x09" * 0x40 Just a test, the DS will error if it recives this

# --- Imports ---
from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from uuid import uuid1
from os.path import exists
import helper
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
            user = models.GSUser.query().filter_by(gsid = request.args['gsid']) # Find the user
            if user.poke_is_sleeping:
                return DREAMING_POKEMON_RESPONSE
            else:
                return PUT_POKE_TO_SLEEP_RESPONSE
        return b"\x08"
    elif request.args["p"] == SAVEDATA_UPLOAD: # Triggered by putting a Pokemon to sleep.
        # Dump
        with open(f"savdata-{request.args['gsid']}.sav", "wb") as f:
            f.write(request.get_data())
        return DREAMING_POKEMON_RESPONSE
    elif request.args["p"] == ACCOUNT_CREATE_UPLOAD:
        with open(f"savdata-{request.args['gsid']}.sav", "wb") as f:
            data = request.get_data()
            f.write(data)
            g5s = helper.Gen5Save(data)
            u = models.GSUser(id=g5s.tid, name=g5s.trainer_name, poke_is_sleeping=False, gsid=request.args['gsid']) # There should be no pokemon sleeping
            db.session.add(u)
            db.session.commit()
        return DREAMING_POKEMON_RESPONSE # Success response
    elif request.args["p"] == WORLDBATTLE_DOWNLOAD: # Live competition
        if exists(f"savdata-{request.args['gsid']}.sav"):
            return Response("no", status=502)
        return DREAMING_POKEMON_RESPONSE # A.k.a "Please use Game Sync Settings"
    elif request.args["p"] == SAVEDATA_DOWNLOAD_FINISH or request.args["p"] == "sleepily.bitlist":
        # User has finished downloading savedata, they should now have a sleeping pokemon
        user = models.GSUser.query().filter_by(gsid = request.args['gsid']) # Find the user
        user.poke_is_sleeping = True
        db.session.add(user)
        db.session.commit()
        return DREAMING_POKEMON_RESPONSE
    elif request.args["p"] == SAVEDATA_DOWNLOAD:
        if exists(f"savdata-{request.args['gsid']}.sav"):
            with open(f"savdata-{request.args['gsid']}.sav", "rb") as f:
                return f.read()
        else:
            return Response("bad gsid", 400)
    else:
        return Response("no", status=502)

@app.route("/")
def index():
    return "Hello there! This page is under construction! Why not check out <a href=\"https://web.archive.org/web/20110715101524id_/http://www.pokemon-gl.com/languages/\">what remains of PGL</a> while you wait?"
# --- Main Block ---
if __name__ == "__main__":
    app.run(host="0.0.0.0")
