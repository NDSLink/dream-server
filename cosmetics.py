# putting this here since it will probably get messy
from flask import Blueprint, render_template
from flask_login import login_required
from json import load

GAMEVER_BW = 0
GAMEVER_B2W2 = 1

cosmetics = Blueprint("cosmetics", __name__)

class GenericContent(object):
    def __init__(self, name, fname, idx, gamever):
        self.name = name
        self.type = "generic"
        self.gamever = gamever
        self.fname = fname
        self._idx = idx
    @classmethod
    def from_json(cls, json_data, gamever):
        return cls(json_data["display_name"], json_data["filename"], json_data["index"], gamever)
class Skin(GenericContent):
    def __init__(self, name, fname, idx, preview_img, gamever):
        super().__init__(name, fname, idx, gamever)
        self.type = "skin"
        self.image_url = preview_img
    @classmethod
    def from_json(cls, json_data, gamever):
        return cls(json_data["display_name"], json_data["filename"], json_data["index"], json_data["preview"], gamever)

class Musical(GenericContent):
    def __init__(self, name, fname, idx, gamever):
        super().__init__(name, fname, idx, gamever)
        self.type = "musical"
    @classmethod
    def from_json(cls, json_data, gamever):
        return cls(json_data["display_name"], json_data["filename"], json_data["index"], gamever)

@cosmetics.route("/select/gear")
@login_required
def select_gear():
    skins = [Skin.from_json(x, GAMEVER_BW) for x in load(open("dls1/CGEAR2/listing.json"))["content"]]
    return render_template("select_gearskin2.html.jinja2", title="Select C-Gear Skin", skins=skins)

