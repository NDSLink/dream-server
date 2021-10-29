from app import db
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import check_password_hash

class GSUser(UserMixin, db.Model):
    __tablename__ = "gsuser"
    id = db.Column(
        db.Integer, primary_key=True
    )  # TODO: create a frontend where you can see GS related info, and download your save, and maybe even edit it
    gsid = db.Column(db.Integer, unique=True)
    # NOTE: this should be pretty easy to implement
    sleeping_pokemon = relationship("Pokemon")
    name = db.Column(db.String(14))
    poke_is_sleeping = db.Column(db.Boolean())
    tid = db.Column(db.Integer)
    password_hash = db.Column(db.String(256))
    # TODO: What else?
    def __repr__(self):
        return "<GSUser %r>" % self.id
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dexno = db.Column(db.Integer)
    name = db.Column(db.String(16))
    level = db.Column(db.Integer)
    exp = db.Column(db.Integer)
    iv_hp = db.Column(db.Integer)
    iv_atk = db.Column(db.Integer)
    iv_def = db.Column(db.Integer)
    iv_spatk = db.Column(db.Integer)
    iv_spdef = db.Column(db.Integer)
    iv_speed = db.Column(db.Integer)
    ev_hp = db.Column(db.Integer)
    ev_atk = db.Column(db.Integer)
    ev_def = db.Column(db.Integer)
    ev_spatk = db.Column(db.Integer)
    ev_spdef = db.Column(db.Integer)
    ev_speed = db.Column(db.Integer)
    nature = db.Column(db.String())
    ability = db.Column(db.String())
    item = db.Column(db.String())
    move1 = db.Column(db.String())
    move2 = db.Column(db.String())
    move3 = db.Column(db.String())
    move4 = db.Column(db.String())
    gsuser_id = db.Column(db.String(), db.ForeignKey("gsuser.id"))
    # TODO: Convert moves into valid pokeapi.cc move names
    # i.e., V-Create becomes v-create, Ice Burn becomes ice-burn
    # There are likely special exceptions to that
    # NOTE:
    # pkapiified_str = 'whatever db.String()'.lower().replace(' ', '-')
    # should work?
