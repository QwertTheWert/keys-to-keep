from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user
from app import db, request

class PaymentPage:
	payment_bp = Blueprint("payment", __name__, template_folder="templates", static_folder="static", static_url_path="/payment/static/")

	def __init__(self, flask_app, bcrypt):

		@self.payment_bp.route('/payment')
		def payment():
			return render_template("payment.html")

		flask_app.register_blueprint(self.payment_bp)