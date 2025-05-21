from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

from werkzeug.middleware.proxy_fix import ProxyFix


db = SQLAlchemy()

def create_app(database_uri='sqlite:///database.db'):
	app = Flask(__name__)

	app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
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
	from blueprints.additional_info import AdditionalInfoPage

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
	AdditionalInfoPage(app, bcrypt)

	@login_manager.user_loader 
	def load_user(user_id):		
		return db.session.get(User, int(user_id))

	# Register error handler for 404
	@app.errorhandler(404)
	def page_not_found(error):
		return render_template('error_template.html'), 404

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
		password= 'password123',
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

	switch_data = [SwitchType(name="Cherry MX Red"), SwitchType(name="Gateron Brown"), SwitchType(name="Kailh Box White")]
	db.session.add_all(switch_data)
	
	keycaps_data = [Keycaps(name="ABS"), Keycaps(name="POM"), Keycaps(name="PBT")]
	db.session.add_all(keycaps_data)


	kb1 = Keyboard(
		name="NOIR TIMELESS82 V2",
		subtitle="75% keyboard with knob, screen, and VIA support",
		description=(
			"This 75% keyboard features a programmable knob, TFT LCD Screen, "
			"gasket mount for a soft typing feel, and supports QMK/VIA for full customization. "
			"It also offers multi-layout flexibility."
		),
		image_url="assets/timeless82v2.png",  # Replace with your actual image path
		switch_type=1,  # Assuming this ID exists in your switch_type table
		keycaps=1,      # Assuming this ID exists in your keycaps table
		discount=10,
		sold=25,
		price=2100000,  # Example in Indonesian Rupiah or adjust as needed
		quantity=50
	)
	kb2 = Keyboard(
		name="VORTEXSERIES SWIFT82",
		subtitle="Hot-swap 82-key compact keyboard",
		description=(
			"The VortexSeries Swift82 features a compact 82-key layout with hot-swappable sockets, "
			"ideal for quick customization and vibrant RGB lighting. Perfect for gamers and coders alike."
		),
		image_url="assets/swift82.png",  # Replace with your actual image path
		switch_type=2,  # Assuming ID 2 exists in your switch_type table (e.g., Kailh Box Pink)
		keycaps=2,      # Assuming ID 2 exists in your keycaps table
		discount=50,    # 50% discount: from 1,299,000 to 659,000
		sold=73,
		price=659000,   # After discount
		quantity=120
	)
	kb3 = Keyboard(
		name="KEYCHRON K8 PRO",
		subtitle="Wireless Mechanical TKL Keyboard",
		description=(
			"The Keychron K8 Pro is a Tenkeyless (TKL) wireless mechanical keyboard that features QMK/VIA "
			"support, hot-swappable switches, and a sleek aluminum frame. Ideal for professionals and enthusiasts "
			"seeking flexibility and premium typing experience."
		),
		image_url="assets/keychron_k8_pro.png",  # Replace with actual file path
		switch_type=3,  # Assuming ID 3 exists in switch_type table (e.g., Gateron Red)
		keycaps=3,      # Assuming ID 3 exists in keycaps table
		discount=20,    # 20% off
		sold=124,
		price=1049000,  # Original price: 1,311,250
		quantity=95
	)

	db.session.add_all([kb1, kb2])
	db.session.commit()
	db.session.add_all([
		Color(name="White & Maroon", keyboard_id=1), 
		Color(name="Navy & Cream", keyboard_id=1), 
		Color(name="Black & Orange", keyboard_id=2),
		Color(name="Dark Gray with Red Accents", keyboard_id=3)])
	
	db.session.add_all([
		Switch(name="Gateron Pro Red", keyboard_id=1), 
		Switch(name="Kailh Box Pink", keyboard_id=2),
		Switch(name="Keychron K Pro Brown", keyboard_id=3)])
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
			image_url=keyboard_images[randint(0,9)],
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