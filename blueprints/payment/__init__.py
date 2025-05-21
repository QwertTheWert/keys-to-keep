from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import current_user
from app import request, db

class PaymentPage:

	def __init__(self, flask_app, bcrypt):
		from models import DeliveryService, Transaction, Review, Keyboard
		payment_bp = Blueprint("payment", __name__, template_folder="templates", static_folder="static", static_url_path="/payment/static/")

		@payment_bp.route('/payment')
		def payment():
			if current_user.is_authenticated:
				data = current_user.get_carts()
				if data["cart_data"]:
					return render_template("payment.html", data=data, user=current_user, delivery_services=DeliveryService.get_all())
				else:
					return redirect(url_for("main_page.main_page"))				
			else:
				return redirect(url_for("login.login"))

		@payment_bp.route('/payment/get_delivery_data', methods=['POST'])
		def get_delivery_data():
			return jsonify({"price" : DeliveryService.get_price(request.get_json()["value"]).price})

		@payment_bp.route('/payment/create_transaction', methods=['POST'])
		def create_transaction():
			data = request.get_json()
			print(data)
			transaction = Transaction(delivery_id=data["delivery_id"], user_id=current_user.id, total_price=data["total_price"])
			db.session.add(transaction)
			db.session.commit()

			carts = [cart_datum["cart"] for cart_datum in current_user.get_carts()["cart_data"]]
			for cart in carts:
				keyboard = Keyboard.get_by_id(cart.keyboard_id)
				keyboard.quantity -= cart.quantity
				Review.create(cart, transaction.id)
				db.session.delete(cart)
			db.session.commit()
			
			return jsonify({"transaction_id" : transaction.id})

		flask_app.register_blueprint(payment_bp)