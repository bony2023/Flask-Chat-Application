from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import Required

class CreateRoom(Form):
	nameC = StringField('Display name', [Required()])
	avatarC = FileField('Avatar <small>(optional)</small>')
	submitC = SubmitField('Create')
	
class JoinRoom(Form):
	nameJ = StringField('Display name', [Required()])
	roomidJ = StringField('Room ID', [Required()])
	avatarJ = FileField('Avatar <small>(optional)</small>')
	submitJ = SubmitField('Join')

class StartAnon(Form):
	submitA = SubmitField('Start chat')
