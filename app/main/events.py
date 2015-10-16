from flask import session
from flask.ext.socketio import emit, join_room, leave_room
from .. import socketio


@socketio.on('joined', namespace='/chat')
def joined(message):
    roomid = session.get('roomid')
    join_room(roomid)
    emit('status', {'msg': session.get('username') + ' entered the room.'}, room=roomid)


@socketio.on('text', namespace='/chat')
def left(message):
	roomid = session.get('roomid')
	emit('message', {'msg': message['msg'], 'user': session.get('username'), 'rid': session.get('roomid'), 'uid': session.get('userid')}, room=roomid)

@socketio.on('left', namespace='/chat')
def left(message):
    roomid = session.get('roomid')
    leave_room(roomid)
    emit('status', {'msg': session.get('username') + ' left the room.'}, room=roomid)