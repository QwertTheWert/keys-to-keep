from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate


db = SQLAlchemy()

def create_app():
	app = Flask(__name__)

	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
	app.secret_key = 'SECRET_KEY'
	app.url_map.strict_slashes = False

	db.init_app(app)

	login_manager = LoginManager()
	login_manager.init_app(app)

	from models import User 
	def load_user(id):
		return User.query.get(id)

	bcrypt = Bcrypt(app)
	
	import blueprints.register.register as register
	import blueprints.login.login as login
	import blueprints.profile.profile as profile
	import blueprints.search.search as search
	import blueprints.product.product as product
	import blueprints.showcase.showcase as showcase

	register.register_to_app(app, bcrypt)
	login.register_to_app(app, bcrypt)
	profile.register_to_app(app, bcrypt)
	search.register_to_app(app, bcrypt)
	product.register_to_app(app, bcrypt)
	showcase.register_to_app(app, bcrypt)

	@login_manager.user_loader 
	def load_user(user):
		return User.query.get(int(user))

	migrate = Migrate(app, db)


	return app

