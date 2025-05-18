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

	from models import User
	def load_user(id):
		return User.query.get(id)

	bcrypt = Bcrypt(app)
	
	from blueprints.cart.cart import CartPage
	from blueprints.login.login import Login
	from blueprints.register.register import Register
	from blueprints.payment.payment import Payment
	from blueprints.product.product import Product
	from blueprints.profile.profile import Profile
	from blueprints.products.products import Products

	Register(app, bcrypt)
	Login(app, bcrypt)
	Product(app, bcrypt)
	Profile(app, bcrypt)
	Products(app, bcrypt)
	CartPage(app, bcrypt)
	Payment(app, bcrypt)

	@login_manager.user_loader 
	def load_user(user):
		return User.query.get(int(user))

	migrate = Migrate(app, db)
	return app

def add_and_commit(db_class):
	db.session.add(db_class)
	db.session.commit()

def format_money(value):
		return '{:,}'.format(value).replace(',', '.')

def create_dummy_data():
	from models import db, User, SwitchType, Keycaps, Keyboard, Switch, Color, Cart, Rating
	import random
	
	user1 = User(
		username='john_doe',
		full_name='John Doe',
		email='john.doe@example.com',
		password='password123',
		bank_number='1234567890'
	)
	user2 = User(
		username='jane_smith',
		full_name='Jane Smith',
		email='jane.smith@example.com',
		password='password456',
		bank_number='0987654321'
	)
	db.session.add_all([user1, user2])
	db.session.commit() 

	switch_data = [SwitchType(name="Switch A"), SwitchType(name="Switch B"), SwitchType(name="Switch C")]
	db.session.add_all(switch_data)
	db.session.commit() 
	
	keycaps_data = [Keycaps(name="Keycaps A"), Keycaps(name="Keycaps B"), Keycaps(name="Keycaps C")]
	db.session.add_all(keycaps_data)
	db.session.commit() 

	keyboard_data = [
			('Mechanical Keyboard', 'A premium mechanical keyboard with red switches and customizable RGB lighting.'),
			('Compact 60% Mechanical Keyboard', 'A small 60% layout mechanical keyboard perfect for portability.'),
			('Full-Sized Mechanical Keyboard', 'Full-sized keyboard with all the necessary keys for a traditional typing experience.'),
			('Wireless Mechanical Keyboard', 'Enjoy the freedom of wireless with mechanical key switches and long battery life.'),
			('Ergonomic Mechanical Keyboard', 'An ergonomic design for those who type long hours, with a split layout.'),
			('Membrane Keyboard', 'A budget-friendly membrane keyboard with quiet keys and basic functionality.'),
			('RGB Mechanical Keyboard', 'A white-themed RGB mechanical keyboard for style-conscious users.'),
			('Gaming Mechanical Keyboard', 'Designed for gamers, with high-speed switches and customizable key lighting.'),
			('Travel Mechanical Keyboard', 'Compact and durable mechanical keyboard perfect for on-the-go users.')
		]
	for i, (name, description) in enumerate(keyboard_data):
		keyboard = Keyboard(
			name=name,
			subtitle=f'{name} for the ultimate typing experience.',
			description=description,
			discount=random.randint(0, 20),
			keycaps=random.randint(1,3),
			switch_type=random.randint(1,3),
			sold=random.randint(1,20),
			quantity=random.randint(1, 20),
			price= (random.randint(2,20) * 50000), 
		)
		db.session.add(keyboard)
		db.session.commit()

		color1 = Color(name="Black", keyboard_id=i+1)
		color2 = Color(name="White", keyboard_id=i+1)
		color3 = Color(name="Silver", keyboard_id=i+1)
		db.session.add_all([color1, color2, color3])
		switch1 = Switch(name="Blue", keyboard_id=i+1)
		switch2 = Switch(name="Red", keyboard_id=i+1)
		switch3 = Switch(name="Brown", keyboard_id=i+1)
		db.session.add_all([switch1, switch2, switch3])	
		db.session.commit()

	# Create Cart entries
	cart1 = Cart(user_id=1, keyboard_id=1, color_id=1, switch_id=2, quantity=2)
	cart2 = Cart(user_id=1, keyboard_id=2, color_id=4, switch_id=6, quantity=1)
	db.session.add_all([cart1, cart2])
	db.session.commit()
	
	rating1 = Rating(user_id=1, keyboard_id=1, rating=5, description='Great keyboard with responsive keys.')
	rating2 = Rating(user_id=2, keyboard_id=2, rating=4, description='Feels great, but could use more clicking noises settings.')
	db.session.add_all([rating1, rating2])

	db.session.commit() 
	
	print("Dummy data created successfully!")