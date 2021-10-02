from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
class GSUser(db.Model):
    id = Column(String, primary_key=True) # TODO: create a frontend where you can see GS related info, and download your save, and maybe even edit it
    # NOTE: this should be pretty easy to implement
    sleeping_pokemon = relationship("Pokemon")
    # TODO: What else?
    def __repr__(self):
        return '<GSUser %r>' % self.id

class Pokemon(db.Model):
    id = Column(Integer, primary_key=True)
    dexno = Column(Integer)
    name = Column(String)
    level = Column(Integer)
    exp = Column(Integer)
    iv_hp = Column(Integer)
    iv_atk = Column(Integer)
    iv_def = Column(Integer)
    iv_spatk = Column(Integer)
    iv_spdef = Column(Integer)
    iv_speed = Column(Integer)
    ev_hp = Column(Integer)
    ev_atk = Column(Integer)
    ev_def = Column(Integer)
    ev_spatk = Column(Integer)
    ev_spdef = Column(Integer)
    ev_speed = Column(Integer)
    nature = Column(String)
    ability = Column(String)
    item = Column(String)
    move1 = Column(String)
    move2 = Column(String)
    move3 = Column(String)
    move4 = Column(String)
    gsuser_id = Column(String, ForeignKey('gsuser.id'))
    # TODO: Convert moves into valid pokeapi.cc move names
    # i.e., V-Create becomes v-create, Ice Burn becomes ice-burn
    # There are likely special exceptions to that
    # NOTE:
    # pkapiified_str = 'whatever string'.lower().replace(' ', '-')
    # should work?
    


