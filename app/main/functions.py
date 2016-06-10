from flask import send_from_directory
import string, random, json
from .models import *
from app import db
import cloudinary, cloudinary.uploader, cloudinary.api
import os
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER_AVATAR

cloudinary.config( 
  cloud_name = "flaskchat", 
  api_key = "376393826937556", 
  api_secret = "l9dzGwmNU4MgKnxTd74sY7-mjBc" 
)

def getRoom(size = 10, chars = string.ascii_uppercase + string.digits):
	while True:
		ret = ''.join(random.choice(chars) for _ in xrange(size))
		if Room.query.filter_by(roomid = ret).first() is None:
			return ret

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
	
def upload(data, filename):
	if data and allowed_file(data.filename):
		response = cloudinary.uploader.upload(data)
		avatar = Avatar(avatarurl = response.get('secure_url'), avatarlocalid = filename)
		db.session.add(avatar)
		db.session.commit()
		
def userAvatar(filename):
	avatar = Avatar.query.filter_by(avatarlocalid = filename).first()
	avatar_url = 'https://res.cloudinary.com/flaskchat/image/upload/v1465554827/tkhdu3vthahiumtu2fop.png'
	if avatar:
		avatar_url = avatar.avatarurl
	return avatar_url

def create_room(form):
	room = getRoom()
	user = form.nameC.data
	r = Room(roomid = room)
	u = User(username = user, inRoom = r)
	db.session.add(r, u)
	db.session.commit()
	return [u.userid, user, room]
	
def join_room(form, room):
	user = form.nameJ.data
	r = Room.query.filter_by(roomid = room).first()
	u = User(username = user, inRoom = r)
	db.session.add(u)
	db.session.commit()
	return [u.userid, user, room]

def getUsers(roomid):
	r = Room.query.filter_by(roomid = roomid).first()
	if r:
		ret = []
		for user in r.users.all():
			ret.append({'id': user.userid, 'name': user.username})
		return json.dumps(ret)
	return None
	
def removeUser(userid, roomid):
	r = Room.query.filter_by(roomid = roomid).all()
	User.query.filter_by(userid = userid).delete()
	if r and len(r[0].users.all()) == 0:
		Room.query.filter_by(roomid = roomid).delete()
	db.session.commit()
	avatar = Avatar.query.filter_by(avatarlocalid = '{}_{}'.format(roomid, userid)).first()
	if avatar:
		cloudinary.uploader.destroy(avatar.avatarurl.split('/')[-1].split('.')[0])

def validRoom(roomid):
	return Room.query.filter_by(roomid = roomid).first() != None