class Product:
	def __init__(self, flask_app, bcrypt):
		from flask import Blueprint, render_template, redirect, url_for, request
		from flask_login import current_user
		from app import db, request
		from models import User

		product_bp = Blueprint("product", __name__, template_folder="templates", static_folder="static")

		@product_bp.route('/product')
		def search():
			return render_template("product.html")

		flask_app.register_blueprint(product_bp)