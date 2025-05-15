from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

from werkzeug.middleware.proxy_fix import ProxyFix

db = SQLAlchemy()

def create_app():
	app = Flask(__name__)

	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
	app.secret_key = 'SECRET_KEY'
	app.url_map.strict_slashes = False
	app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1, x_port=1, x_prefix=1)

	db.init_app(app)

	

	login_manager = LoginManager()
	login_manager.init_app(app)

	from models import User, ProductCategory
	def load_user(id):
		return User.query.get(id)

	bcrypt = Bcrypt(app)
	
	from blueprints.cart.cart import Cart
	from blueprints.login.login import Login
	from blueprints.register.register import Register
	from blueprints.payment.payment import Payment
	from blueprints.product.product import Product
	from blueprints.profile.profile import Profile
	from blueprints.search.search import Search
	from blueprints.products.products import Products

	Register(app, bcrypt)
	Login(app, bcrypt)
	Product(app, bcrypt)
	Profile(app, bcrypt)
	Search(app, bcrypt)
	Products(app, bcrypt)
	Cart(app, bcrypt)
	Payment(app, bcrypt)

	@login_manager.user_loader 
	def load_user(user):
		return User.query.get(int(user))

	migrate = Migrate(app, db)


	return app

