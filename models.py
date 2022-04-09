from app import db
from sqlalchemy.orm import relationship
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    gsuser = db.relationship('GSUser', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class GSUser(db.Model):
    __tablename__ = "gsuser"
    id = db.Column(
        db.Integer, primary_key=True
    )  # TODO: create a frontend where you can see GS related info, and download your save, and maybe even edit it
    tid = db.Column(db.Integer)
    # NOTE: this should be pretty easy to implement
    name = db.Column(db.String(14))
    poke_is_sleeping = db.Column(db.Boolean())
    gender = db.Column(db.Integer, default=0) # 0 = male, 1 = female (I think? Don't know yet so it just defaults to 0)
    gamever = db.Column(db.Integer) # 20 = white, 21 = black, 22 = white 2, 23 = black 2
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    # TODO: What else?
    def __repr__(self):
        return "<GSUser %r>" % self.id
