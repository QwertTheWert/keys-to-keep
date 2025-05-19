from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user
from app import db, request, format_money

class PaymentPage:
	payment_bp = Blueprint("payment", __name__, template_folder="templates", static_folder="static", static_url_path="/payment/static/")

	def __init__(self, flask_app, bcrypt):
		from models import Item, Color, Switch 

		@self.payment_bp.route('/payment')
		def payment():
			if current_user.is_authenticated:
				carts = current_user.get_carts()
				keyboards = [cart.get_keyboard().get_data() for cart in carts]
				subtotal = [keyboards[i]["keyboard"].get_discounted_price() * carts[i].quantity for i in range(len(carts)) ]
				total = sum(subtotal)
				data = {
					"carts": carts,
					"keyboards": keyboards,
					"color": [Item.get(Color, cart.color_id) for cart in carts],
					"switch": [Item.get(Switch, cart.switch_id) for cart in carts],
					"subtotal" : [ format_money(i) for i in subtotal ],
					"total" : format_money(total)
				}
			return render_template("payment.html", data=data, user=current_user)

		flask_app.register_blueprint(self.payment_bp)