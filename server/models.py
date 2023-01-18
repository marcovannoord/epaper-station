# models.py

from flask_login import UserMixin
from . import db
from sqlalchemy.sql import func


class User(UserMixin, db.Model):
    id = db.Column(
        db.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    admin = db.Column(db.Boolean())


# class Platform(db.Model):
#     id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
#     name = db.Column(db.String(100), unique=True)
#     version = db.Column(db.String(100))
#     uploaded = db.Column(db.DateTime)
#     notes = db.Column(db.String(1000)) # add any notes about the platform
#     devices = db.relationship('Device', backref='platform', lazy=True)
#     file = db.Column(db.String(100))
#     downloads = db.Column(db.Integer, default = 0)


class Device(db.Model):
    id = db.Column(
        db.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    mac = db.Column(db.String(23), nullable=False)  # aa:bb:cc:dd:de:ff
    protover = db.Column(db.Integer)  # protocol version?
    hw_type = db.Column(db.Integer)
    sw_ver = db.Column(db.Integer)
    screen_px_width = db.Column(db.Integer)
    screen_px_height = db.Column(db.Integer)
    screen_mm_width = db.Column(db.Integer)
    screen_mm_height = db.Column(db.Integer)
    compressions_supported = db.Column(db.Integer)
    max_wait_mSec = db.Column(db.Integer)
    screen_type = db.Column(db.Integer)
    rfu = db.Column(db.String)
    first_seen = db.Column(db.DateTime, server_default=func.now())
    last_seen = db.Column(db.DateTime, server_default=func.now())
    last_packet_LQI = db.Column(db.Integer)
    last_packet_RSSI = db.Column(db.Integer)
    temperature = db.Column(db.Integer)
    battery_voltage = db.Column(db.Integer)
