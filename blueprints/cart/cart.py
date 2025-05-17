from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import current_user
from app import db, request
from models import Cart, Product, ProductModel

class Cart:
	cart_bp = Blueprint("cart", __name__, template_folder="templates", static_folder="static", static_url_path="/cart/static/")

	def __init__(self, flask_app, bcrypt):
		from models import Cart, Product, ProductModel

		@self.cart_bp.route('/cart')		
		def cart():
			if current_user.is_authenticated:
				cart_data = []
				total = 0
				carts = db.session.query(Cart).filter(Cart.user_id == current_user.id).all()
				for cart in carts:
					product_model = db.session.query(ProductModel).filter(ProductModel.id == cart.product_model_id).first()
					product = db.session.query(Product).filter(Product.id == product_model.product_id).first()
					price_after_discount =  int(product_model.price * (product.discount / 100))
					subtotal = price_after_discount * cart.quantity
					cart_data.append({
						"product_model" : product_model,
						"product" : product,
						"cart" : cart,
						"is_max" : cart.quantity == product_model.quantity,
						"price" : self.format_money(price_after_discount),
						"subtotal" : self.format_money(price_after_discount),
					})
					total += subtotal
				return render_template("cart.html", cart_data=cart_data, total=self.format_money(total))
			else:
				return redirect(url_for("login.login"))
		
		@self.cart_bp.route('/cart/increment_quantity', methods=['POST'])
		def increment_quantity():
			return  self.update_quantity(request.get_json(), "increment")

		@self.cart_bp.route('/cart/set_quantity', methods=['POST'])
		def set_quantity():
			return self.update_quantity(request.get_json(), "set")
		
		@self.cart_bp.route('/cart/remove', methods=['POST'])
		def remove():
			data = request.get_json()
			cart = db.session.query(Cart).filter(Cart.id == data["cart_id"]).first()
			product_model = db.session.query(ProductModel).filter(ProductModel.id == cart.product_model_id).first()
			product = db.session.query(Product).filter(Product.id == product_model.product_id).first()

			substotal = int((product_model.price * (product.discount / 100)) * cart.quantity)
			new_total = int(data["total"]) - substotal
			db.session.delete(cart)
			db.session.commit()
			return jsonify({"new_total" : self.format_money(new_total)})
		
		flask_app.register_blueprint(self.cart_bp)

	def update_quantity(self, data, type):
		from models import Cart, Product, ProductModel
		cart = db.session.query(Cart).filter(Cart.id == data["cart_id"]).first()
		product_model = db.session.query(ProductModel).filter(ProductModel.id == cart.product_model_id).first()
		product = db.session.query(Product).filter(Product.id == product_model.product_id).first()

		old_quantity = cart.quantity
		if type == "increment":
			cart.quantity += 1 if data['action'] == "increase" else -1
		elif type == "set":
			cart.quantity = int(data['value']) if int(data['value']) <= product_model.quantity else product_model.quantity
		
		new_substotal = int((product_model.price * (product.discount / 100)) * cart.quantity)
		new_total = int(data["total"]) - int((product_model.price * (product.discount / 100)) * (old_quantity - cart.quantity))
		status = ""
		if cart.quantity >= product_model.quantity:
			status = "max"
		if cart.quantity <= 0:
			status = "min"

		db.session.commit()
		return jsonify({'new_quantity': cart.quantity, "new_subtotal" : self.format_money(new_substotal), "new_total" : self.format_money(new_total), "status": status})

	def format_money(self,value):
		return '{:,}'.format(value).replace(',', '.')