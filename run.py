#!flask/bin/python
from app import create_app, socketio
from gevent import monkey
monkey.patch_all()

app = create_app()

if __name__ == '__main__':
	socketio.run(app)