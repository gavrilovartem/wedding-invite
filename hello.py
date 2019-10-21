from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

application = Flask(__name__)
application.config.from_object(Config)
db = SQLAlchemy(application)
migrate = Migrate(application, db)
login = LoginManager(application)
#login.login_view = 'cabinet'
bootstrap = Bootstrap(application)


# -*- coding: utf-8 -*-
from application  import application , db
from application .models import User, Alcohol, Music, Wish, UserChoice

@application.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Alcohol': Alcohol, 'Music': Music, 'Wish': Wish, 'UserChoice': UserChoice}

from application import routes, models


if __name__ == "__main__":
   application.run(host='0.0.0.0')