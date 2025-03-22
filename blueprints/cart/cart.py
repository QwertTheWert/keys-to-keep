from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user
from app import db, request

class Product:
	cart_bp = Blueprint("cart", __name__, template_folder="templates", static_folder="static")

	def __init__(self, flask_app, bcrypt):

		@self.cart_bp.route('/cart')
		def cart():
			return render_template("cart.html")

		flask_app.register_blueprint(self.cart_bp)