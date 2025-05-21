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
	
	from blueprints.main_page import MainPage
	from blueprints.cart import CartPage
	from blueprints.login import LoginPage
	from blueprints.register import RegisterPage
	from blueprints.payment import PaymentPage
	from blueprints.keyboard import KeyboardPage
	from blueprints.profile import ProfilePage
	from blueprints.marketplace import MarketplacePage
	from blueprints.complete import CompletePage
	from blueprints.compare import ComparePage
	from blueprints.review import ReviewPage

	MainPage(app, bcrypt)
	RegisterPage(app, bcrypt)
	LoginPage(app, bcrypt)
	KeyboardPage(app, bcrypt)
	ProfilePage(app, bcrypt)
	MarketplacePage(app, bcrypt)
	CartPage(app, bcrypt)
	PaymentPage(app, bcrypt)
	CompletePage(app, bcrypt)
	ComparePage(app, bcrypt)
	ReviewPage(app, bcrypt)

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
	from models import db, User, SwitchType, Keycaps, Keyboard, Switch, Color, Cart, Review, DeliveryService
	from datetime import datetime, timedelta, timezone
	from random import randint

	now = datetime.now(timezone.utc)
	
	user1 = User(
		username='john_doe',
		full_name='John Doe',
		email='john.doe@example.com',
		password='password123',
		address='Home Street, 123'
	)
	user2 = User(
		username='jane_smith',
		full_name='Jane Smith',
		email='jane.smith@example.com',
		password='password456',
		address='West Land, 456'
	)

	user3 = User(
		username='Bob',
		full_name='Bob Smith',
		email='Bob@Bob.com',
		password='$2b$12$vXRNQvdIOG2f4G03Bx77qerhCe8chHqq1HdFxpn9ABhTF0KBEqb8e',
		address='Bob Road to the west of the Road Land, 456'
	)

	db.session.add_all([user1, user2, user3])

	switch_data = [SwitchType(name="Switch A"), SwitchType(name="Switch B"), SwitchType(name="Switch C")]
	db.session.add_all(switch_data)
	
	keycaps_data = [Keycaps(name="Keycaps A"), Keycaps(name="Keycaps B"), Keycaps(name="Keycaps C")]
	db.session.add_all(keycaps_data)

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
	keyboard_images = [
		"assets/keyboards_images/Ajazz-AK820-Max-With-Display-Stray-Night-600x600.jpeg",
		"assets/keyboards_images/ajazzAK870SC.jpg",
		"assets/keyboards_images/aulaF75.webp",
		"assets/keyboards_images/Fantech%20ATOM%20PRO83%20MK913.jpg",
		"assets/keyboards_images/LANGTU%20GK65.webp",
		"assets/keyboards_images/noirSpade65.webp",
		"assets/keyboards_images/ROVER84_Lightyear.webp",
		"assets/keyboards_images/Voyager68_V2.webp",
		"assets/keyboards_images/xera87.jpg",
		"assets/keyboards_images/zifriendZA68.jpg"
	]
	for i, (name, description) in enumerate(keyboard_data):
		keyboard = Keyboard(
			name=name,
			subtitle=f'{name} for the ultimate typing experience.',
			description=description,
			discount=randint(0, 20),
			keycaps=randint(1,3),
			switch_type=randint(1,3),
			sold=randint(1,20),
			quantity=randint(1, 20),
			price= (randint(2,20) * 50000), 
			date_added=now - timedelta(days=randint(5,30)),
			image_url=keyboard_images[randint(0,10)],
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


		rev1 = Review(user_id=1, keyboard_id=i+1, switch_id=randint(1,3), color_id=randint(1,3), rating=5, description='Great keyboard with responsive keys.')
		rev2 = Review(user_id=2, keyboard_id=i+1, switch_id=randint(1,3), color_id=randint(1,3), rating=4, description='Feels great, but could use more clicking noises settings.')
		rev3 = Review(user_id=1, keyboard_id=i+1, switch_id=randint(1,3), color_id=randint(1,3), rating=3, description='Eh, its mid, but it works.')
		rev4 = Review(user_id=2, keyboard_id=i+1, switch_id=randint(1,3), color_id=randint(1,3), rating=1, description='This is Horrible! Dont buy it!!!')
		db.session.add_all([rev1 if randint(1,2) == 1 else rev3, rev2 if randint(1,2) == 1 else rev4])

	# Create Cart entries
	cart1 = Cart(user_id=1, keyboard_id=1, color_id=1, switch_id=2, quantity=2)
	cart2 = Cart(user_id=1, keyboard_id=2, color_id=4, switch_id=6, quantity=1)
	db.session.add_all([cart1, cart2])
	
	


	deliveryservices = [
		DeliveryService(name="Instant (1-2 hours)", price="50000"),
		DeliveryService(name="Regular (1-3 days)", price="20000"),
		DeliveryService(name="Economy (4-7 days)", price="10000"),
	]
	db.session.add_all(deliveryservices)


	db.session.commit()
	print("Dummy data created successfully!")