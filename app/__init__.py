from flask import Flask
from flask.ext.socketio import SocketIO
from flask.ext.sqlalchemy import SQLAlchemy

socketio = SocketIO()
db = SQLAlchemy()

def create_app(debug = True):
	app = Flask(__name__)
	app.debug = debug
	app.config.from_object('config')
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)
	db.init_app(app)
	with app.app_context():
		db.create_all()
	socketio.init_app(app)
	return app
