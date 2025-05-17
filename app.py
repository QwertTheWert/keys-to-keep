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
	
	# from blueprints.cart.cart import Cart
	# from blueprints.login.login import Login
	# from blueprints.register.register import Register
	# from blueprints.payment.payment import Payment
	# from blueprints.product.product import Product
	# from blueprints.profile.profile import Profile
	# from blueprints.search.search import Search
	# from blueprints.products.products import Products

	# Register(app, bcrypt)
	# Login(app, bcrypt)
	# Product(app, bcrypt)
	# Profile(app, bcrypt)
	# Search(app, bcrypt)
	# Products(app, bcrypt)
	# Cart(app, bcrypt)
	# Payment(app, bcrypt)

	@login_manager.user_loader 
	def load_user(user):
		return User.query.get(int(user))

	migrate = Migrate(app, db)
	return app

# def create_dummy_data():
# 	from models import db, User, ProductCategory, Keyboard, ProductModel, Cart, Rating
# 	import random
 
# 	# Create Product Categories
# 	category_keyboards = ProductCategory(name='Keyboards')
# 	category_accessories = ProductCategory(name='Accessories')
	
# 	# Add categories to the session
# 	db.session.add_all([category_keyboards, category_accessories])
# 	db.session.commit()  # Commit to create category entries in the database
	
# 	# Create Users
# 	user1 = User(
# 		username='john_doe',
# 		full_name='John Doe',
# 		email='john.doe@example.com',
# 		password='password123',  # Normally hash the password
# 		bank_number='1234567890'
# 	)
	
# 	user2 = User(
# 		username='jane_smith',
# 		full_name='Jane Smith',
# 		email='jane.smith@example.com',
# 		password='password456',  # Normally hash the password
# 		bank_number='0987654321'
# 	)
# 	# Add users to the session
# 	db.session.add_all([user1, user2])
# 	db.session.commit()  # Commit cart entries to the database

# 	# Create Products
# 	keyboard_data = [
# 			('Mechanical Keyboard', 'A premium mechanical keyboard with red switches and customizable RGB lighting.'),
# 			('Compact 60% Mechanical Keyboard', 'A small 60% layout mechanical keyboard perfect for portability.'),
# 			('Full-Sized Mechanical Keyboard', 'Full-sized keyboard with all the necessary keys for a traditional typing experience.'),
# 			('Wireless Mechanical Keyboard', 'Enjoy the freedom of wireless with mechanical key switches and long battery life.'),
# 			('Ergonomic Mechanical Keyboard', 'An ergonomic design for those who type long hours, with a split layout.'),
# 			('Membrane Keyboard', 'A budget-friendly membrane keyboard with quiet keys and basic functionality.'),
# 			('RGB Mechanical Keyboard', 'A white-themed RGB mechanical keyboard for style-conscious users.'),
# 			('Gaming Mechanical Keyboard', 'Designed for gamers, with high-speed switches and customizable key lighting.'),
# 			('Travel Mechanical Keyboard', 'Compact and durable mechanical keyboard perfect for on-the-go users.')
# 		]
# 	# Create Products for Keyboards
# 	products = []
# 	for i, (name, description) in enumerate(keyboard_data):
# 		product = Keyboard(
# 			category_id=1,  # Keyboards category
# 			name=name,
# 			subtitle=f'{name} for the ultimate typing experience.',
# 			description=description,
# 			discount=random.randint(0, 20)  # Random discount between 0 and 20%
# 		)
# 		products.append(product)
# 	db.session.add_all(products)
# 	db.session.commit() 
 
#  # Create Product Models
# 	keyboard_model_data = [
# 			('Red', 1, 300000),
# 			('Blue', 1, 300000),
# 			('Yellow', 1, 300000),
# 			('Beige', 2, 200000),
# 			('White', 2, 200000),
# 			('Black', 3, 500000),
# 			('White', 3, 500000),
# 			('Black', 4, 600000),
# 			('White', 4, 600000),
# 			('White', 4, 600000),
# 			('White', 4, 600000),
# 			('Green', 5, 450000),
# 			('Blue', 5, 450000),
# 			('Pink', 6, 150000),
# 			('Cyan', 6, 150000),
# 			('Black', 7, 750000),
# 			('Grey', 7, 750000),
# 			('RGB', 8, 950000),
# 			('Regular', 8, 900000),
# 			('Blue', 9, 650000),
# 			('Silver', 9, 650000),
# 		]
# 	# Create Product Models for Keyboards
# 	product_models = []
# 	for i, (name, product_id, price) in enumerate(keyboard_model_data):
# 		model = ProductModel(
# 			product_id=product_id,
# 			name=name,
# 			price=price,
# 			quantity=random.randint(1, 20)  # Random discount between 0 and 20%
# 		)
# 		product_models.append(model)
# 	db.session.add_all(product_models)
# 	db.session.commit() 

	
# 	# Create Cart entries
# 	cart1 = Cart(user_id=1, product_model_id=1, quantity=2)  # John adds 2 Mechanical Keyboards
# 	cart2 = Cart(user_id=1, product_model_id=2, quantity=1)  # Jane adds 1 Gaming Mouse
	
# 	# Add carts to the session
# 	db.session.add_all([cart1, cart2])
# 	db.session.commit()  # Commit cart entries to the database
	
# 	# # Create Ratings
# 	rating1 = Rating(
# 		user_id=1,  # John
# 		product_id=1,  # Mechanical Keyboard
# 		rating=5,
# 		description='Great keyboard with responsive keys.'
# 	)
	
# 	rating2 = Rating(
# 		user_id=2,  # Jane
# 		product_id=2,  # Gaming Mouse
# 		rating=4,
# 		description='Feels great, but could use more clicking noises settings.'
# 	)
	
# 	# Add ratings to the session
# 	db.session.add_all([rating1, rating2])
# 	db.session.commit()  # Commit ratings to the database
	
# 	print("Dummy data created successfully!")