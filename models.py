'''
MIT License

Copyright (c) 2022 DSLink Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
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
