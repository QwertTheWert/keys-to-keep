from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import current_user
from app import db, request, format_money
from models import Cart

class CartPage:
	cart_bp = Blueprint("cart", __name__, template_folder="templates", static_folder="static", static_url_path="/cart/static/")

	def __init__(self, flask_app, bcrypt):
		from models import Cart, Keyboard

		@self.cart_bp.route('/cart')		
		def cart():
			if current_user.is_authenticated:
				return render_template("cart.html", data=current_user.get_carts())
			else:
				return redirect(url_for("login.login"))
		
		@self.cart_bp.route('/cart/update_quantity', methods=['POST'])
		def update_quantity():
			data = request.get_json()
			cart = Cart.get_by_id(int(data["cart_id"]))
			cart_data = cart.get_data()
			keyboard_data = cart_data["keyboard_data"]
			
			if data["type"] == "increment":
				cart.quantity += 1 if data['action'] == "increase" else -1
			elif data["type"] == "set":
				cart.quantity = int(data['value']) if int(data['value']) <= keyboard_data["keyboard"].quantity else keyboard_data["keyboard"].quantity
			db.session.commit()
			
			status = ""
			if cart.quantity >= keyboard_data["keyboard"].quantity:
				status = "max"
			if cart.quantity <= 0:
				status = "min"

			new_cart_data = cart.get_data()
			return jsonify({'new_quantity': cart.quantity, "new_subtotal" : new_cart_data["subtotal"], "new_total" : current_user.get_total(), "status": status})
		
		@self.cart_bp.route('/cart/remove', methods=['POST'])
		def remove():
			data = request.get_json()
			cart = Cart.get_by_id(data["cart_id"])
			db.session.delete(cart)
			db.session.commit()
			return jsonify({"new_total" : current_user.get_total()})
		
		flask_app.register_blueprint(self.cart_bp)