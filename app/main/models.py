from app import db

class Room(db.Model):
	roomid = db.Column(db.String(12), primary_key=True)
	users = db.relationship('User', backref='inRoom', lazy='dynamic')
	
class User(db.Model):
	userid = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30))
	roomid = db.Column(db.String(12), db.ForeignKey('room.roomid'))