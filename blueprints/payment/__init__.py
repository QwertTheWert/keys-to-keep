from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import current_user
from app import db, request, format_money

class PaymentPage:
	payment_bp = Blueprint("payment", __name__, template_folder="templates", static_folder="static", static_url_path="/payment/static/")

	def __init__(self, flask_app, bcrypt):
		from models import DeliveryService

		@self.payment_bp.route('/payment')
		def payment():
			if current_user.is_authenticated:
				return render_template("payment.html", data=current_user.get_carts(), user=current_user, delivery_services=DeliveryService.get_all())
			else:
				return redirect(url_for("login.login"))

		@self.payment_bp.route('/payment/get_delivery_data', methods=['POST'])
		def get_delivery_data():
			return jsonify({"price" : DeliveryService.get_price(request.get_json()["value"]).price})

		flask_app.register_blueprint(self.payment_bp)