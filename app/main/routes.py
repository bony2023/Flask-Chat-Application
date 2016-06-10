from flask import render_template, url_for, redirect, session, request, flash, jsonify
from .forms import CreateRoom, JoinRoom, StartAnon
from .functions import *
from . import main
import os

@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
	create = CreateRoom()
	join = JoinRoom()
	anon = StartAnon()
	if create.validate_on_submit():
		session['userid'], session['username'], session['roomid'] = create_room(create)
		upload(request.files['avatarC'], session['roomid'] + '_' + str(session['userid']))
		return redirect(url_for('.chat'))
	elif join.validate_on_submit():
		if not validRoom(join.roomidJ.data):
			flash('%s is not a valid Room ID. Try again or create new room.' %join.roomidJ.data)
			return redirect('/')
		session['userid'], session['username'], session['roomid'] = join_room(join, join.roomidJ.data)
		upload(request.files['avatarJ'], session['roomid'] + '_' + str(session['userid']))
		return redirect(url_for('.chat'))
	elif session.get('userid', '') != '':
		return redirect(url_for('.chat'))
	return render_template('index.html', namespace='/', createform=create, joinform=join, anonform=anon)
	
@main.route('/chat')
def chat():
	if session.get('userid', '') == '':
		return redirect('/')
	elif request.is_xhr:
		return jsonify({
			'uid': session.get('userid')
		})
	return render_template('chat.html', namespace='/chat')
	
@main.route('/getAvatar/<filename>')
def getAvatar(filename):
	if request.is_xhr:
		return jsonify({
			'url': userAvatar(filename)
		})
	
@main.route('/getUsers')
def RoomMembers():
	if session.get('userid', '') == '':
		return redirect('/')
	elif request.is_xhr:
		return jsonify({
			'users': getUsers(session.get('roomid'))
		})

@main.route('/exit')
def exit():
	if session.get('userid', '') == '':
		return redirect('/')
	elif request.is_xhr:
		userid = session.get('userid')
		roomid = session.get('roomid')
		removeUser(userid, roomid)
		session.clear()
		return jsonify({
			'status': 'ok'
		})