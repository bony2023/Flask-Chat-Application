import os
from app import create_app, socketio
from gevent import monkey
monkey.patch_all()

app = create_app()

if __name__ == '__main__':
	port = int(os.getenv('VCAP_APP_PORT', '5000'))
	socketio.run(app, host='0.0.0.0', port=port)