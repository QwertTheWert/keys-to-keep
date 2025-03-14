from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()

def create_app():
	app = Flask(__name__)

	import blueprints.register.register as register

	register.register_to_app(app)

	
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
	
	db.init_app(app)

	# migrate = Migrate(app, db)

	return app

