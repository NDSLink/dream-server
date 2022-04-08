from app import db, redis
import models
from forms import *
import helper
from flask import (
    request,
    send_from_directory,
    render_template,
    redirect,
    url_for,
    Response,
    Blueprint,
)

from wtforms import ValidationError

from pickle import dumps
from gsid import gsid_dec, gsid_enc
from os.path import exists
from werkzeug.security import generate_password_hash

# import redis
from constants import *
from flask_babel import _

main_routes = Blueprint("main_routes", __name__)


@main_routes.route("/dsio/gw", methods=["GET", "POST"])
def gw():
    if request.args["p"] == PLAYSTATUS:
        if exists(
            f"savdata-{request.args['gsid']}.sav"
        ):
            user = models.GSUser.query.filter_by(
                id=request.args["gsid"]
            ).first()  # Find the user
            if user == None:
                with open(f"savdata-{request.args['gsid']}.sav", "rb") as f:
                    g5s = helper.Gen5Save(f)
                    if not models.GSUser.query.filter_by(tid=g5s.tid).first():
                        user = models.GSUser(
                            id=request.args["gsid"],
                            tid=g5s.tid,
                            name=g5s.trainer_name,
                            poke_is_sleeping=False,
                            gamever=request.args["rom"]
                        )
                        db.session.add(user)
                        db.session.commit()
                    redis.publish(
                        "savedesync", request.args["gsid"]
                    )  # Save was desynced. Inform any subbed clients to ensure that data is resynced.
                    return b"\x08"
            if user.poke_is_sleeping:
                print("is sleeping: yeah")
                return WAKE_UP_AND_DOWNLOAD
            else:
                print("is not sleeping: nah")
                return b"\x00"
        return b"\x08"
    elif request.args["p"] == SAVEDATA_UPLOAD:
        user = models.GSUser.query.filter_by(
            id=request.args["gsid"]
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
                    id=request.args["gsid"],
                    name=g5s.trainer_name,
                    poke_is_sleeping=False,
                    tid=g5s.tid,
                    gamever=request.args["rom"]
                )
                db.session.add(u)
                db.session.commit()
                redis.publish("newacct", request.args["gsid"])
            except:
                redis.publish("newacct", request.args["gsid"])
                pass  # It's an alt save.
        return DREAMING_POKEMON_RESPONSE  # Success response
    #elif request.args["p"] == WORLDBATTLE_DOWNLOAD:  # Live competition
    #    if exists(f"savdata-{request.args['gsid']}.sav"):
    #        return Response("worldbattle is unimplemented lol", status=502)
    #    return DREAMING_POKEMON_RESPONSE  # A.k.a "Please use Game Sync Settings"
    elif request.args["p"] == SAVEDATA_DOWNLOAD_FINISH:
        redis.publish("finishdl", request.args["gsid"])
        user = models.GSUser.query.filter_by(
            id=request.args["gsid"]
        ).first()  # Find the user
        user.poke_is_sleeping = False
        db.session.add(user)
        db.session.commit()
        return DREAMING_POKEMON_RESPONSE
    elif request.args["p"] == SLEEPILY_BITLIST:
        return b"\x00\x00\x00\x00" + (b"\x00" * 0x7C) + (b"\xff" * 0x80)
    elif request.args["p"] == SAVEDATA_DOWNLOAD:
        if exists(f"savdata-{request.args['gsid']}.sav"):
            user = models.GSUser.query.filter_by(id=request.args["gsid"]).first()
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
            # Byte 0x01 = If not zero, triggers 1320x, where x is the number
            # Byte 0x02 = Triggers comm error if not zero
            # Byte 0x03 = Triggers comm error if not zero
            # Byte 0x04 = Triggers comm error if not zero
            # Byte 0x05-0x80 onward = padding
            ret = ret + b"\x00\x00\x00\x00" + (b"\x00" * 0x7C)
            #ret = ret + b"\xff\xff\xff\xff"
            # Byte 0x81-0xD1(?) = Pokemon
            # Pokemon Structure:
            # Byte 0x00-0x01 = Species
            # Byte 0x02-0x03 = ???
            # Byte 0x04-0x05 = ???
            # Byte 0x06-0x07 = ???
            # Byte 0x08 = ???
            ret = ret + b"\x01\x01\x01\x01\x01\x01\x01\x01" * 10  # 10 8-byte pokemon
            # Byte 0xD2-0xD5 = flags or smthn idk
            ret = ret + b"\x01\x01\x01\x01"  # Up to 20 4-byte items (2-bytes index, 2-bytes count)

            return ret
        else:
            print("Bad GSID! Response dump:")
            print(f"Tok: {request.args['tok']}")
            print(f"GSID: {request.args['gsid']}")
            return Response("bad gsid", 400)
    elif request.args["p"] == SAVEDATA_GETBW:
        with open(f"savdata-{request.args['gsid']}.sav", "rb") as f:
            return f.read()
    elif request.args["p"] == WORLDBATTLE_DOWNLOAD:
        with open(f"savdata-{request.args['gsid']}.sav", "rb") as f:
            return b"\x00\x00\x00\x00" + (b"\x00" * 0x7C) + (b"\xff" * 0x80)
    elif request.args["p"] == WORLDBATTLE_UPLOAD:
        return b"\x00\x00\x00\x00" + (b"\x00" * 0x7C) + (b"\xff" * 0x80)
    else:
        return Response("no", status=400)


@main_routes.route("/")
def home():
    # return 'Hello there! This page is under construction! Why not check out <a href="https://web.archive.org/web/20110715101524id_/http://www.pokemon-gl.com/languages/">what remains of PGL</a> while you wait?'
    return render_template("home.html.jinja2", title=_("Home"))


@main_routes.route("/savedata", methods=["GET", "POST"])
def savedata():
    form = LinkForm()
    if form.validate_on_submit():
        return redirect(url_for("main_routes.get_savedata", trainerid=gsid_dec(form.gsid.data)))
    return render_template(
        "savedata.html.jinja2", form=form, title=_("Manage Save Data")
    )


@main_routes.route("/savedata/<trainerid>")
def get_savedata(trainerid):
    u = models.GSUser.query.filter_by(id=trainerid).first()
    if u == None:
        if exists(f"savdata-{trainerid}.sav"):
            return send_from_directory(".", f"savdata-{trainerid}.sav")
    return send_from_directory(".", f"savdata-{u.id}.sav")


@main_routes.route("/dreamland/iod")
def island_of_dreams():
    return render_template("island_of_dreams.html.jinja2", title=_("Island of Dreams"))


# @app.route("/users")
# def users():
#    return f"Hello! To view user information, go to {url_for('users')}/<your GSID>. For instance, if your GSID is AAAAAAA2EE, go to {url_for('users')}/AAAAAAA2EE. Note: this will have a better look soon!"

@main_routes.route("/SakeStorageServer/StorageServer.asmx", methods=["POST"])
def sake_storage_server():
    # basic sake server
    print(request.data)
    return '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
   xmlns:xsd="http://www.w3.org/2001/XMLSchema">
<soap:Body>
<GetMyRecordsResponse xmlns="http://gamespy.net/sake">
<GetMyRecordsResult>Success</GetMyRecordsResult>
<values><ArrayOfRecordValue>
<RecordValue><binaryDataValue><value>bkflhglksfghsdfjghskldfogh</value></binaryDataValue></RecordValue>
</ArrayOfRecordValue></values>
</GetMyRecordsResponse>
</soap:Body>
</soap:Envelope>''' if b"NUM_WIFICUP_WIN_COUNTER" not in request.data else '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
   xmlns:xsd="http://www.w3.org/2001/XMLSchema">
<soap:Body>
<GetMyRecordsResponse xmlns="http://gamespy.net/sake">
<GetMyRecordsResult>Success</GetMyRecordsResult>
<values><ArrayOfRecordValue>
<RecordValue><binaryDataValue><value>1</value></binaryDataValue></RecordValue>
<RecordValue><binaryDataValue><value>1</value></binaryDataValue></RecordValue>
<RecordValue><binaryDataValue><value>1</value></binaryDataValue></RecordValue>
<RecordValue><binaryDataValue><value>1</value></binaryDataValue></RecordValue>
<RecordValue><binaryDataValue><value>1</value></binaryDataValue></RecordValue>
<RecordValue><binaryDataValue><value>1</value></binaryDataValue></RecordValue>
<RecordValue><binaryDataValue><value>1</value></binaryDataValue></RecordValue>
</ArrayOfRecordValue></values>
</GetMyRecordsResponse>
</soap:Body>
'''

@main_routes.route("/download", methods=["GET", "POST"])
def download():
    # basic dls1 for DEBUGGING ONLY
    print(request.form)
    if request.form["action"] == "bGlzdA**":
        if request.form['attr1'] == "UkVHQ0FSRF9F":
            # grab regcards
            return "4011_IC04_Master_en.bin						NAAIZ6Qw8zC-MPwwyjC3MOcwyjDrMAAw8YKeig**					REGCARD_E					4011					352\r\n"
        #elif request.form["attr1"] == "TVVTSUNBTF9F":
            #return "M010_munna_1_e_02.bin						8YKeit8w5TD8MLgwqzDrMAAw4DDzMMow					MUSICAL_E					10					352\r\n"
        else:
            return Response("", status=404)
    elif request.form["action"] == "Y29udGVudHM*":
        resp = send_from_directory(".", "4011_IC04_Master_en.bin")
        resp.headers["Content-Type"] = "application/x-dsdl"
        return resp
    #return "4011_IC04_Master_en.bin	NAAIZ6Qw8zC-MPwwyjC3MOcwyjDrMAAw8YKeig**\tREGCARD_E\t4011\t\t352"
@main_routes.route("/users/<gsid>")
def user_gsid(gsid):
    u = models.GSUser.query.filter_by(id=gsid_dec(gsid)).first()
    return render_template("user.html.jinja2", title=_("User ") + u.name, user=u)

@main_routes.route("/link")
def link_gsid():
    form = LinkPwForm()
    if form.validate_on_submit():
        gu = models.GSUser.query.filter_by(id=gsid_dec(form.gsid.data)).first()
        if gu == None:
            raise ValidationError("Invalid GSID! Please use Game Sync Settings to set up Game Sync.")
        u = models.User.query.filter_by(gsuser=gu).first()
        if u != None:
            raise ValidationError("This GSID is already linked to a user!")
        u = models.User(name=gu.name, gsuser=gu, password=generate_password_hash(form.password.data))
        db.session.add(u)
        db.session.commit()
        return redirect(url_for("main_routes.home"))