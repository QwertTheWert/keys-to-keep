from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import current_user
from app import db, request, format_money
from models import Cart, Keyboard

class Cart:
	cart_bp = Blueprint("cart", __name__, template_folder="templates", static_folder="static", static_url_path="/cart/static/")

	def __init__(self, flask_app, bcrypt):
		from models import Cart, Keyboard

		@self.cart_bp.route('/cart')		
		def cart():
			if current_user.is_authenticated:
				cart_data = []
				total = 0
				carts = current_user.get_carts()
				for cart in carts:
					keyboard : Keyboard = cart.get_keyboard()
					price_after_discount =  keyboard.get_discounted_price()
					subtotal = price_after_discount * cart.quantity
					cart_data.append({
						"keyboard" : keyboard,
						"cart" : cart,
						"is_max" : cart.quantity == keyboard.quantity,
						"price" : format_money(price_after_discount),
						"subtotal" : format_money(subtotal),
					})
					total += subtotal
				return render_template("cart.html", cart_data=cart_data, total=format_money(total))
			else:
				return redirect(url_for("login.login"))
		
		@self.cart_bp.route('/cart/increment_quantity', methods=['POST'])
		def increment_quantity():
			return  update_quantity(request.get_json(), "increment")

		@self.cart_bp.route('/cart/set_quantity', methods=['POST'])
		def set_quantity():
			return update_quantity(request.get_json(), "set")
		
		@self.cart_bp.route('/cart/remove', methods=['POST'])
		def remove():
			data = request.get_json()
			cart = Cart.get_by_id(data["cart_id"])
			keyboard = cart.get_keyboard()

			price_after_discount =  keyboard.get_discounted_price()
			subtotal = price_after_discount * cart.quantity
			new_total = int(data["total"]) - subtotal

			cart.delete()
			return jsonify({"new_total" : format_money(new_total)})
		
		flask_app.register_blueprint(self.cart_bp)

def update_quantity(data, type):
	cart = Cart.get_cart_by_id(data["cart_id"])
	keyboard = cart.get_keyboard()

	old_quantity = cart.quantity
	if type == "increment":
		cart.quantity += 1 if data['action'] == "increase" else -1
	elif type == "set":
		cart.quantity = int(data['value']) if int(data['value']) <= keyboard.quantity else keyboard.quantity
	
	price_after_discount =  keyboard.get_discounted_price()
	new_substotal = price_after_discount * cart.quantity
	new_total = int(data["total"]) - (price_after_discount * (old_quantity - cart.quantity))
	status = ""
	if cart.quantity >= keyboard.quantity:
		status = "max"
	if cart.quantity <= 0:
		status = "min"

	db.session.commit()
	return jsonify({'new_quantity': cart.quantity, "new_subtotal" : format_money(new_substotal), "new_total" : format_money(new_total), "status": status})

