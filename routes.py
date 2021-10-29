
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

from app import app, db, redis
import models
from forms import *
import helper
from flask import request, send_from_directory, render_template, redirect, url_for, Response
from pickle import dumps
from gsid import gsid_dec
from os import exists
import redis

@app.route("/dsio/gw", methods=["GET", "POST"])
def gw():
    if request.args["p"] == PLAYSTATUS:
        if exists(
            f"savdata-{request.args['gsid']}.sav"
        ):  # Check if trainer has registered with the server
            user = models.GSUser.query.filter_by(
                gsid=request.args["gsid"]
            ).first()  # Find the user
            if user == None:
                with open(f"savdata-{request.args['gsid']}.sav", "rb") as f:
                    g5s = helper.Gen5Save(f)
                    user = models.GSUser(
                        id=g5s.tid,
                        name=g5s.trainer_name,
                        poke_is_sleeping=False,
                        gsid=request.args["gsid"],
                    )
                    db.session.add(user)
                    db.session.commit()
                    redis.publish(
                        "savedesync", request.args["gsid"]
                    )  # Save was desynced. Inform any subbed clients to ensure that data is resynced.

            if user.poke_is_sleeping:
                return WAKE_UP_AND_DOWNLOAD
            else:
                return PUT_POKE_TO_SLEEP_RESPONSE
        return b"\x08"
    elif request.args["p"] == SAVEDATA_UPLOAD:
        user = models.GSUser.query.filter_by(
            gsid=request.args["gsid"]
        ).first()  # Find the user
        user.poke_is_sleeping = True
        db.session.add(user)
        db.session.commit()
        redis.publish(
            "pokemonhotel",
            dumps({"gsid": request.args["gsid"], "name": user.name}),
        )
        with open(f"savdata-{request.args['gsid']}.sav", "wb") as f:
            f.write(request.get_data())
        return DREAMING_POKEMON_RESPONSE
    elif request.args["p"] == ACCOUNT_CREATE_UPLOAD:
        with open(f"savdata-{request.args['gsid']}.sav", "wb") as f:
            data = request.get_data()
            f.write(data)
            try:
                g5s = helper.Gen5Save(data)
                u = models.GSUser(
                    id=g5s.tid,
                    name=g5s.trainer_name,
                    poke_is_sleeping=False,
                    gsid=request.args["gsid"],
                )
                db.session.add(u)
                db.session.commit()
                redis.publish("newacct", request.args["gsid"])
            except:
                redis.publish("newacct", request.args["gsid"])
                pass  # It's an alt save.
        return DREAMING_POKEMON_RESPONSE  # Success response
    elif request.args["p"] == WORLDBATTLE_DOWNLOAD:  # Live competition
        if exists(f"savdata-{request.args['gsid']}.sav"):
            return Response("worldbattle is unimplemented lol", status=502)
        return DREAMING_POKEMON_RESPONSE  # A.k.a "Please use Game Sync Settings"
    elif request.args["p"] == SAVEDATA_DOWNLOAD_FINISH:
        redis.publish("finishdl", request.args["gsid"])
        user = models.GSUser.query.filter_by(
            gsid=request.args["gsid"]
        ).first()  # Find the user
        user.poke_is_sleeping = False
        db.session.add(user)
        db.session.commit()
        return DREAMING_POKEMON_RESPONSE
    elif request.args["p"] == SLEEPILY_BITLIST:
        return b"\x00\x00\x00\x00" + (b"\x00" * 0x7C) + (b"\xff" * 0x80)
    elif request.args["p"] == SAVEDATA_DOWNLOAD:
        if exists(f"savdata-{request.args['gsid']}.sav"):
            user = models.GSUser.query.filter_by(gsid=request.args["gsid"]).first()
            # it runs the following math function 10 times, increasing x each time:  f[x] = (x * 0x08) + 0x04, each time it runs that function, it checks the 2 bytes at that location in the response, if those are \x00\x00 then break the loop, otherwise if d <= 0x1ed where D is the data just pulled, then do something(!)
            # According to mm201, it's reading 8 bytes from that location???
            # ret = [0] * 0x5a
            # ret = [0] * 0x5a
            ret = b""
            # for i in range(0, 80, 8):
            # 4 shorts for species number (0x1ed = 493 = arceus natdex number)
            #    ret[i - 8] = 255
            #    ret[i - 7] = 13
            #    ret[i - 6] = 0x00
            #    ret[i - 5] = 0x00
            #    # Move
            #    ret[i - 4] = 1
            #    # Gender
            #    ret[i - 3] = 0x00
            #    # Animation
            #    ret[i - 2] = 0x00
            # Area
            #    ret[i - 1] = 0x00
            # 3 flags: 0x58, 0x57, 0x59
            # ret[0x58] = 0xff
            # ret[0x57] = 0xff
            # ret[0x59] = 0xff
            # Attempt 2!
            # for i in range(0, 80, 8):
            #    ret[i] = 0x89
            #    ret[i + 1] = 0x00
            #    ret[i + 2] = 0x67
            #    ret[i + 3] = 0x00
            #    ret[i + 4] = 0x86
            #    ret[i + 5] = 0xB9
            #    ret[i + 6] = 0x7D
            #    ret[i + 7] = 0x34

            # Now the data has been built.
            # Enjoy understanding this.
            # NOTE: None of the above works.
            # ret = ret + b"\x00\x00\x00\x00" + (b"\x00" * 0x7C)
            # ret = ret + b"\x00\x00\x00\x00"
            # ret = ret + b"\x00" * 0x57
            # ret = ret + b"\xFF\x00\x00"
            # ret = ret + b"\x02\x4F"
            # ret = bytearray(ret)
            # ret[0xa6] = 0xff # Download C-GEAR skins (additionally, it'll put GS into "mode 2")
            # The last byte is the number of item
            # Each item is a set of 4 bytes
            # The first 2 bytes are a 16-bit int containing the item ID
            redis.publish("dlstart", request.args["gsid"])
            # return ret
            ret = ret + b"\x00\x00\x00\x00" + (b"\x00" * 0x7C)
            ret = ret + b"\x00\x00\x00\x00"
            ret = ret + b"\x00" * 0x57
            ret = ret + b"\x01" * 80
            ret = ret + b"\x01" * 80
            return DREAMING_POKEMON_RESPONSE
        else:
            print("Bad GSID! Response dump:")
            print(f"Tok: {request.args['tok']}")
            print(f"GSID: {request.args['gsid']}")
            return Response("bad gsid", 400)
    else:
        return Response("no", status=400)


@app.route("/")
def home():
    # return 'Hello there! This page is under construction! Why not check out <a href="https://web.archive.org/web/20110715101524id_/http://www.pokemon-gl.com/languages/">what remains of PGL</a> while you wait?'
    return render_template("home.html.jinja2", title="Home")


@app.route("/savedata", methods=["GET", "POST"])
def savedata():
    form = LinkForm()
    if form.validate_on_submit():
        return redirect(url_for("get_savedata", trainerid=gsid_dec(form.gsid.data)))
    return render_template("savedata.html.jinja2", form=form, title="Manage Save Data")


@app.route("/savedata/<trainerid>")
def get_savedata(trainerid):
    u = models.GSUser.query.filter_by(id=trainerid).first()
    if u == None:
        if exists(f"savdata-{trainerid}.sav"):
            return send_from_directory(".", f"savdata-{trainerid}.sav")
    return send_from_directory(".", f"savdata-{u.gsid}.sav")


@app.route("/users")
def users():
    return f"Hello! To view user information, go to {url_for('users')}/<your GSID>. For instance, if your GSID is AAAAAAA2EE, go to {url_for('users')}/AAAAAAA2EE. Note: this will have a better look soon!"


@app.route("/users/<gsid>")
def user_gsid():
    return f"wip!"