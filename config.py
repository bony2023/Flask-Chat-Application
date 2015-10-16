import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
UPLOAD_FOLDER_AVATAR = os.path.join(basedir, 'uploads/avatar/')
ALLOWED_EXTENSIONS = set(['gif', 'png', 'jpeg', 'jpg'])
WTF_CSRF_ENABLED = True
SECRET_KEY = '7fc9f8133ca143bb973255f94256111d'
