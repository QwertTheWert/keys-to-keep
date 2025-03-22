from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user
from app import db, request
from models import User

class Product:
	
	product_bp = Blueprint("product", __name__, template_folder="templates", static_folder="static")
	
	def __init__(self, flask_app, bcrypt):
		@self.product_bp.route('/product')
		def search():
			return render_template("product.html")

		flask_app.register_blueprint(self.product_bp)