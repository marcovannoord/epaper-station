# models.py

from datetime import datetime
from flask_login import UserMixin
from . import db
from sqlalchemy.sql import func

from collections import namedtuple

TagInfo = namedtuple(
    "TagInfo",
    """
protoVer,
swVer,
hwType,
batteryMv,
rfu1,
screenPixWidth,
screenPixHeight,
screenMmWidth,
screenMmHeight,
compressionsSupported,
maxWaitMsec,
screenType,
rfu
""",
)

CheckinInfo = namedtuple(
    "CheckinInfo",
    """
swVer,
hwType,
batteryMv,
lastPacketLQI,
lastPacketRSSI,
temperature,
rfu,
""",
)

PendingInfo = namedtuple(
    "PendingInfo",
    """
imgUpdateVer,
imgUpdateSize,
osUpdateVer,
osUpdateSize,
nextCheckinDelay,
rfu
""",
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
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
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    name = db.Column(db.String)
    mac = db.Column(db.String(17), nullable=False)  # aa:bb:cc:dd:de:ff
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


def update_CheckinInfo(src_addr: str, checkinInfo: CheckinInfo) -> Device:
    device: Device = Device.query.filter_by(mac=src_addr.lower()).first()
    if not device:
        device = Device(mac=src_addr.lower())
        print("Device not yet known: {}".format(src_addr))
        db.session.add(device)

    device.last_seen = datetime.utcnow()
    device.battery_voltage = checkinInfo.batteryMv
    device.hw_type = checkinInfo.hwType
    device.last_packet_LQI = checkinInfo.lastPacketLQI
    device.last_packet_RSSI = checkinInfo.lastPacketRSSI
    device.temperature = checkinInfo.temperature - 127
    device.rfu = checkinInfo.rfu
    db.session.commit()
    return device


def update_TagInfo(src_addr: str, tagInfo: TagInfo) -> Device:
    device: Device = Device.query.filter_by(mac=src_addr.lower()).first()
    if not device:
        device = Device(mac=src_addr.lower())
        print("Device not yet known: {}".format(src_addr))
        db.session.add(device)
    
    device.last_seen = datetime.utcnow()
    device.battery_voltage = tagInfo.batteryMv
    device.hw_type = tagInfo.hwType
    device.compressions_supported = tagInfo.compressionsSupported
    device.screen_mm_height = tagInfo.screenMmHeight
    device.screen_mm_width = tagInfo.screenMmWidth
    device.screen_px_height = tagInfo.screenPixHeight
    device.screen_px_width = tagInfo.screenPixWidth
    device.protover = tagInfo.protoVer
    device.sw_ver = tagInfo.swVer
    device.screen_type = tagInfo.screenType
    device.max_wait_mSec = tagInfo.maxWaitMsec
    device.rfu = tagInfo.rfu
    db.session.commit()
    return device


def update_and_get(src_addr: str) -> Device:
    device = Device.query.filter_by(mac=src_addr.lower()).first()
    if device:
        # device already exists, updating
        print("Device already known: {}".format(src_addr))
        device.last_seen = datetime.utcnow()
    else:
        device = Device(mac=src_addr.lower())
        # add the new device to the database
        db.session.add(device)
        print("Adding new device: {}".format(src_addr))
    db.session.commit()
    return device
