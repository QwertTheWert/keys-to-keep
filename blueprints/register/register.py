from app import db, request
from flask_login import login_user, current_user
from flask import Blueprint, render_template, redirect, url_for
from models import User 
from models import ProductCategory, Product, ProductModel, Cart

class Register:
	
	register_bp = Blueprint("register", __name__, template_folder="templates")
	
	def __init__(self, flask_app, bcrypt):
		
		@self.register_bp.route('/register', methods=["GET", "POST"])
		def register():
			message = ""
			full_name = request.form.get("full_name")
			username = request.form.get("username")
			email = request.form.get("email")
			password = request.form.get("password")
			bank_number = request.form.get("bank_number")
			hashed_password = bcrypt.generate_password_hash(password) if password else ""
			if request.method == "POST":
				validation_results = self.validate_data(username, email)
				if validation_results["valid"]:
					self.create_user(full_name, username, email, hashed_password, bank_number)
					return redirect(url_for("register.index"))
				else:
					message = validation_results["reason"]
			return render_template('register.html', message=message, full_name=full_name, username=username, email=email, password=password, bank_number=bank_number)

		@self.register_bp.route('/')
		def index():
			# category = [
			# 	ProductCategory(name="Key Caps"),
			# 	ProductCategory(name="Keyboard"),
			# 	ProductCategory(name="Accessory"),
			# ]
			# db.session.bulk_save_objects(category)
			# products = [
			# 	Product(category_id=1, name="Key Caps A"),
			# 	Product(category_id=1, name="Key Caps B"),
			# 	Product(category_id=2, name="Keyboard A"),
			# 	Product(category_id=2, name="Keyboard B"),
			# 	Product(category_id=3, name="Accessory A"),
			# 	Product(category_id=3, name="Accessory B"),
			# ]
			# db.session.bulk_save_objects(products)

			# product_models = [
			# 	ProductModel(product_id=1, name="Key Caps A1", price="20000", quantity=30),
			# 	ProductModel(product_id=1, name="Key Caps A2", price="21000", quantity=29),
			# 	ProductModel(product_id=2, name="Key Caps B1", price="35000", quantity=18),
			# 	ProductModel(product_id=2, name="Key Caps B2", price="41000", quantity=19),
				
			# 	ProductModel(product_id=3, name="Keyboard A1", price="200000", quantity=30),
			# 	ProductModel(product_id=3, name="Keyboard A2", price="210000", quantity=29),
			# 	ProductModel(product_id=4, name="Keyboard B1", price="350000", quantity=18),
			# 	ProductModel(product_id=4, name="Keyboard B2", price="410000", quantity=19),
				
			# 	ProductModel(product_id=5, name="Accessory A1", price="40000", quantity=10),
			# 	ProductModel(product_id=5, name="Accessory A2", price="41000", quantity=7),
			# 	ProductModel(product_id=6, name="Accessory B1", price="65000", quantity=28),
			# 	ProductModel(product_id=6, name="Accessory B2", price="61000", quantity=17),
			# ]
			# db.session.bulk_save_objects(product_models)
			# db.session.commit()
			if current_user.is_authenticated:
				print(str(current_user.username))
			else:
				print("No user")

			return render_template("main_page.html")
		
		@self.register_bp.route('/dummy')
		def dummy():
			# category = [
			# 	ProductCategory(name="Key Caps"),
			# 	ProductCategory(name="Keyboard"),
			# 	ProductCategory(name="Accessory"),
			# ]
			# db.session.bulk_save_objects(category)
			# products = [
			# 	Product(category_id=1, name="Key Caps A"),
			# 	Product(category_id=1, name="Key Caps B"),
			# 	Product(category_id=2, name="Keyboard A"),
			# 	Product(category_id=2, name="Keyboard B"),
			# 	Product(category_id=3, name="Accessory A"),
			# 	Product(category_id=3, name="Accessory B"),
			# ]
			# db.session.bulk_save_objects(products)

			# product_models = [
			# 	ProductModel(product_id=1, name="Key Caps A1", price="20000", quantity=30),
			# 	ProductModel(product_id=1, name="Key Caps A2", price="21000", quantity=29),
			# 	ProductModel(product_id=2, name="Key Caps B1", price="35000", quantity=18),
			# 	ProductModel(product_id=2, name="Key Caps B2", price="41000", quantity=19),
				
			# 	ProductModel(product_id=3, name="Keyboard A1", price="200000", quantity=30),
			# 	ProductModel(product_id=3, name="Keyboard A2", price="210000", quantity=29),
			# 	ProductModel(product_id=4, name="Keyboard B1", price="350000", quantity=18),
			# 	ProductModel(product_id=4, name="Keyboard B2", price="410000", quantity=19),
				
			# 	ProductModel(product_id=5, name="Accessory A1", price="40000", quantity=10),
			# 	ProductModel(product_id=5, name="Accessory A2", price="41000", quantity=7),
			# 	ProductModel(product_id=6, name="Accessory B1", price="65000", quantity=28),
			# 	ProductModel(product_id=6, name="Accessory B2", price="61000", quantity=17),
			# ]
			# db.session.bulk_save_objects(product_models)
			

			# db.session.bulk_save_objects([
			# 	Cart(user_id=1, product_model_id=1, quantity=12),
			# 	Cart(user_id=1, product_model_id=5, quantity=1),
			# 	Cart(user_id=1, product_model_id=9, quantity=5),
			# ])
			db.session.commit()
			return "Dummy Added"

		flask_app.register_blueprint(self.register_bp)
	
	

	
	def validate_data(self, username, email):
		select_by_username = db.session.execute(db.select(User).filter_by(username=username)).scalar_one_or_none()
		select_by_email = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()
		return_json = { "valid": False, "reason": "" }
		return_json["valid"] = select_by_username is None and select_by_email is None
		if not return_json["valid"]:
			print(select_by_username, select_by_email)
			return_json["reason"] = "Username is taken. Please use another one." if select_by_username is not None else "Email is taken. Please use another one."
		return return_json

	def create_user(self, full_name, username, email, password, bank_number):
		new_user = User(full_name=full_name, username=username, email=email, password=password, bank_number=bank_number)
		db.session.add(new_user)
		db.session.commit()
		login_user(new_user)